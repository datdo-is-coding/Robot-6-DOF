function FOC_Servo_HMI
    % =========================================================================
    % SIEMENS SIMATIC / INDUSTRIAL AC SERVO COMMISSIONING SUITE (MATLAB)
    % Chuẩn giao diện HMI điều khiển Servo công nghiệp cho STM32G473 FOC-PMSM
    % Nền tảng: Native High-Performance MATLAB Graphics (Hiển thị biểu đồ 100%)
    % Dải tốc độ tối đa 1000 RPM & Phanh chủ động khựng cứng trục tức thì
    % =========================================================================

    % Dọn sạch các timer cũ tránh xung đột
    old_timers = timerfind('Tag', 'FOC_HMI_TIMER');
    if ~isempty(old_timers)
        stop(old_timers);
        delete(old_timers);
    end

    % Bảng màu công nghiệp Siemens WinCC / Anthracite Dark Theme
    COLOR_BG       = [0.12, 0.14, 0.17]; % Nền ngoài xám đậm
    COLOR_PANEL    = [0.18, 0.20, 0.24]; % Khung panel con
    COLOR_DARK_BOX = [0.08, 0.10, 0.12]; % Màn hình hiển thị số đen sâu
    COLOR_ACCENT   = [0.00, 0.75, 0.65]; % Xanh ngọc Siemens
    COLOR_CYAN     = [0.00, 0.85, 1.00]; % Cyan Process Value
    COLOR_YELLOW   = [1.00, 0.80, 0.15]; % Vàng Setpoint
    COLOR_GREEN    = [0.10, 0.90, 0.30]; % Xanh lá RUN / OK
    COLOR_RED      = [0.90, 0.15, 0.15]; % Đỏ FAULT / E-STOP
    COLOR_GRAY_DIM = [0.28, 0.30, 0.34]; % Xám viền / đèn tắt
    COLOR_BTN      = [0.25, 0.28, 0.33]; % Màu nút tiêu chuẩn

    % Khởi tạo Cửa sổ chính
    fig = figure('Name', 'SIEMENS SIMATIC - INDUSTRIAL AC SERVO CONTROLLER [STM32G473]', ...
                 'Position', [50, 30, 1180, 720], ...
                 'Color', COLOR_BG, ...
                 'MenuBar', 'none', ...
                 'ToolBar', 'none', ...
                 'NumberTitle', 'off', ...
                 'InvertHardcopy', 'off', ...
                 'CloseRequestFcn', @(~,~) exit_hmi());

    % Biến trạng thái runtime
    s_port = [];
    is_connected = false;
    current_mode = 0; % 0: Pos, 1: Vel, 2: Torque
    is_servo_on = true;
    rx_accumulator = '';

    % Buffer dữ liệu Scope (120 mẫu)
    buf_len = 120;
    x_data = 1:buf_len;
    y_actual = zeros(1, buf_len);
    y_target = zeros(1, buf_len);
    y_effort = zeros(1, buf_len);

    % =========================================================================
    % 1. TOP HEADER - INDUSTRIAL STATUS & CONTROL BAR
    % =========================================================================
    pnl_top = uipanel('Parent', fig, 'Units', 'pixels', 'Position', [15, 645, 1150, 65], ...
                      'BackgroundColor', [0.15, 0.17, 0.20], 'BorderType', 'line', 'HighlightColor', COLOR_ACCENT);

    uicontrol('Parent', pnl_top, 'Style', 'text', 'String', 'SIEMENS', ...
              'Position', [15, 12, 145, 38], 'BackgroundColor', [0.15, 0.17, 0.20], ...
              'ForegroundColor', COLOR_ACCENT, 'FontSize', 22, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    uicontrol('Parent', pnl_top, 'Style', 'text', 'String', 'SINAMICS S210 / FOC-PMSM SERVO SUITE (1000 RPM)', ...
              'Position', [165, 20, 340, 22], 'BackgroundColor', [0.15, 0.17, 0.20], ...
              'ForegroundColor', [0.9, 0.95, 1.0], 'FontSize', 11, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    % Đèn trạng thái công nghiệp (Status Pilot Lamps)
    lamp_ready = uicontrol('Parent', pnl_top, 'Style', 'text', 'String', 'READY', ...
                           'Position', [520, 18, 65, 26], 'BackgroundColor', COLOR_GRAY_DIM, ...
                           'ForegroundColor', 'w', 'FontSize', 9, 'FontWeight', 'bold');

    lamp_run = uicontrol('Parent', pnl_top, 'Style', 'text', 'String', 'SERVO ON', ...
                         'Position', [595, 18, 75, 26], 'BackgroundColor', COLOR_GRAY_DIM, ...
                         'ForegroundColor', 'w', 'FontSize', 9, 'FontWeight', 'bold');

    lamp_in_pos = uicontrol('Parent', pnl_top, 'Style', 'text', 'String', 'IN-POS', ...
                            'Position', [680, 18, 65, 26], 'BackgroundColor', COLOR_GRAY_DIM, ...
                            'ForegroundColor', 'w', 'FontSize', 9, 'FontWeight', 'bold');

    lamp_at_spd = uicontrol('Parent', pnl_top, 'Style', 'text', 'String', 'AT-SPD', ...
                            'Position', [755, 18, 65, 26], 'BackgroundColor', COLOR_GRAY_DIM, ...
                            'ForegroundColor', 'w', 'FontSize', 9, 'FontWeight', 'bold');

    lamp_fault = uicontrol('Parent', pnl_top, 'Style', 'text', 'String', 'FAULT', ...
                           'Position', [830, 18, 65, 26], 'BackgroundColor', COLOR_GRAY_DIM, ...
                           'ForegroundColor', 'w', 'FontSize', 9, 'FontWeight', 'bold');

    % Nút E-STOP Dừng khẩn cấp màu đỏ viền vàng chuẩn tủ điện
    uicontrol('Parent', pnl_top, 'Style', 'pushbutton', 'String', '⛔ E-STOP', ...
              'Position', [1010, 10, 125, 45], 'BackgroundColor', COLOR_RED, ...
              'ForegroundColor', 'y', 'FontSize', 13, 'FontWeight', 'bold', ...
              'Callback', @(~,~) emergency_stop());

    % =========================================================================
    % 2. KHUNG TRÁI: ĐỒNG HỒ TACHOMETER, MÀN HÌNH SỐ & TREND SCOPE (100% HIỂN THỊ)
    % =========================================================================
    pnl_left = uipanel('Parent', fig, 'Units', 'pixels', 'Position', [15, 15, 730, 615], ...
                       'BackgroundColor', COLOR_PANEL, 'Title', '  DRIVE REAL-TIME SUPERVISION & TREND  ', ...
                       'FontWeight', 'bold', 'FontSize', 11, 'ForegroundColor', COLOR_ACCENT, ...
                       'BorderType', 'line', 'HighlightColor', [0.25, 0.28, 0.33]);

    % Đồng hồ kim Tachometer đo tốc độ (Vẽ bằng axes đồ họa trực tiếp)
    ax_gauge = axes('Parent', pnl_left, 'Units', 'pixels', 'Position', [25, 430, 180, 155], ...
                    'Color', COLOR_PANEL, 'XColor', 'none', 'YColor', 'none');
    hold(ax_gauge, 'on');
    th_arc = linspace(-pi/4, 5*pi/4, 100);
    plot(ax_gauge, 0.95*cos(th_arc), 0.95*sin(th_arc), 'Color', [0.3, 0.35, 0.4], 'LineWidth', 4);
    th_rev = linspace(3*pi/4, 5*pi/4, 30);
    plot(ax_gauge, 0.95*cos(th_rev), 0.95*sin(th_rev), 'Color', [0.2, 0.6, 0.9], 'LineWidth', 4);
    th_fwd = linspace(-pi/4, pi/4, 30);
    plot(ax_gauge, 0.95*cos(th_fwd), 0.95*sin(th_fwd), 'Color', COLOR_RED, 'LineWidth', 4);
    line_needle = plot(ax_gauge, [0, 0], [0, 0.8], 'Color', COLOR_YELLOW, 'LineWidth', 2.8);
    plot(ax_gauge, 0, 0, 'o', 'MarkerFaceColor', 'w', 'MarkerEdgeColor', 'k', 'MarkerSize', 6);
    axis(ax_gauge, [-1.1, 1.1, -0.6, 1.1]);
    axis(ax_gauge, 'off');

    uicontrol('Parent', pnl_left, 'Style', 'text', 'String', 'TACHOMETER (±1000 RPM)', ...
              'Position', [30, 415, 170, 18], 'BackgroundColor', COLOR_PANEL, ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold');

    % Bảng màn hình hiển thị số LED (Digital 7-segment style Display)
    pnl_dig = uipanel('Parent', pnl_left, 'Units', 'pixels', 'Position', [225, 420, 485, 175], ...
                      'BackgroundColor', COLOR_DARK_BOX, 'BorderType', 'line', 'HighlightColor', [0.25, 0.3, 0.35]);

    uicontrol('Parent', pnl_dig, 'Style', 'text', 'String', 'ACTUAL POSITION:', ...
              'Position', [15, 138, 140, 22], 'BackgroundColor', COLOR_DARK_BOX, ...
              'ForegroundColor', [0.7, 0.75, 0.8], 'FontSize', 10, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
    lbl_act_pos = uicontrol('Parent', pnl_dig, 'Style', 'text', 'String', '+0.00 °  [0.00 Turns]', ...
                            'Position', [165, 135, 305, 26], 'BackgroundColor', COLOR_DARK_BOX, ...
                            'ForegroundColor', COLOR_CYAN, 'FontSize', 16, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    uicontrol('Parent', pnl_dig, 'Style', 'text', 'String', 'ACTUAL VELOCITY:', ...
              'Position', [15, 98, 140, 22], 'BackgroundColor', COLOR_DARK_BOX, ...
              'ForegroundColor', [0.7, 0.75, 0.8], 'FontSize', 10, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
    lbl_act_vel = uicontrol('Parent', pnl_dig, 'Style', 'text', 'String', '+0.0 RPM  [0.0 rad/s]', ...
                            'Position', [165, 95, 305, 26], 'BackgroundColor', COLOR_DARK_BOX, ...
                            'ForegroundColor', COLOR_GREEN, 'FontSize', 16, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    uicontrol('Parent', pnl_dig, 'Style', 'text', 'String', 'TARGET SETPOINT:', ...
              'Position', [15, 58, 140, 22], 'BackgroundColor', COLOR_DARK_BOX, ...
              'ForegroundColor', [0.7, 0.75, 0.8], 'FontSize', 10, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
    lbl_tar_val = uicontrol('Parent', pnl_dig, 'Style', 'text', 'String', '0.00 °', ...
                            'Position', [165, 55, 305, 26], 'BackgroundColor', COLOR_DARK_BOX, ...
                            'ForegroundColor', COLOR_YELLOW, 'FontSize', 16, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    uicontrol('Parent', pnl_dig, 'Style', 'text', 'String', 'VOLTAGE / EFFORT:', ...
              'Position', [15, 18, 140, 22], 'BackgroundColor', COLOR_DARK_BOX, ...
              'ForegroundColor', [0.7, 0.75, 0.8], 'FontSize', 10, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
    lbl_vq_info = uicontrol('Parent', pnl_dig, 'Style', 'text', 'String', 'Vq: 0.00 V | Bus: 24.0 Vdc', ...
                            'Position', [165, 16, 305, 24], 'BackgroundColor', COLOR_DARK_BOX, ...
                            'ForegroundColor', [0.9, 0.6, 1.0], 'FontSize', 13, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    % Scope 1: Live Tracking Trace (Setpoint vs Process Value)
    ax_scope = axes('Parent', pnl_left, 'Units', 'pixels', 'Position', [55, 155, 655, 240], ...
                    'Color', [0.06, 0.08, 0.10], 'XColor', [0.65, 0.7, 0.75], 'YColor', [0.65, 0.7, 0.75]);
    grid(ax_scope, 'on');
    ax_scope.GridColor = [0.25, 0.3, 0.35];
    ax_scope.GridAlpha = 0.8;
    title(ax_scope, 'SERVO REAL-TIME RESPONSE TRACE (100 Hz)', 'Color', 'w', 'FontSize', 10, 'FontWeight', 'bold');
    xlabel(ax_scope, 'Samples (100 Hz)', 'Color', [0.7, 0.7, 0.7], 'FontSize', 9);
    ylabel(ax_scope, 'Tracking Value', 'Color', [0.7, 0.7, 0.7], 'FontSize', 9);
    hold(ax_scope, 'on');

    line_tar = plot(ax_scope, x_data, y_target, 'Color', [1.0, 0.35, 0.35], 'LineStyle', '--', 'LineWidth', 2.0, 'DisplayName', 'Target SP');
    line_act = plot(ax_scope, x_data, y_actual, 'Color', COLOR_CYAN, 'LineStyle', '-', 'LineWidth', 2.2, 'DisplayName', 'Actual PV');
    legend(ax_scope, 'Location', 'northwest', 'TextColor', 'w', 'Color', [0.12, 0.14, 0.17], 'EdgeColor', [0.3, 0.35, 0.4]);

    % Scope 2: Control Effort (Vq voltage)
    ax_effort = axes('Parent', pnl_left, 'Units', 'pixels', 'Position', [55, 30, 655, 95], ...
                     'Color', [0.06, 0.08, 0.10], 'XColor', [0.65, 0.7, 0.75], 'YColor', [0.65, 0.7, 0.75]);
    grid(ax_effort, 'on');
    ax_effort.GridColor = [0.25, 0.3, 0.35];
    ax_effort.GridAlpha = 0.8;
    xlabel(ax_effort, 'Samples', 'Color', [0.7, 0.7, 0.7], 'FontSize', 8);
    ylabel(ax_effort, 'Vq (V)', 'Color', [0.7, 0.7, 0.7], 'FontSize', 8);
    ylim(ax_effort, [-10, 10]);
    hold(ax_effort, 'on');
    line_eff = plot(ax_effort, x_data, y_effort, 'Color', [0.9, 0.5, 1.0], 'LineWidth', 1.8);

    % =========================================================================
    % 3. KHUNG PHẢI: BẢNG ĐIỀU KHIỂN VẬN HÀNH (OPERATOR PANEL)
    % =========================================================================
    pnl_right = uipanel('Parent', fig, 'Units', 'pixels', 'Position', [760, 15, 405, 615], ...
                        'BackgroundColor', COLOR_PANEL, 'Title', '  OPERATOR CONTROL STATION  ', ...
                        'FontWeight', 'bold', 'FontSize', 11, 'ForegroundColor', COLOR_ACCENT, ...
                        'BorderType', 'line', 'HighlightColor', [0.25, 0.28, 0.33]);

    % Cổng truyền thông
    uicontrol('Parent', pnl_right, 'Style', 'text', 'String', 'PORT:', ...
              'Position', [15, 558, 50, 22], 'BackgroundColor', COLOR_PANEL, ...
              'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    edt_port = uicontrol('Parent', pnl_right, 'Style', 'edit', 'String', '/dev/ttyACM1', ...
                         'Position', [70, 555, 190, 28], 'BackgroundColor', 'w', ...
                         'FontSize', 10, 'FontWeight', 'bold');

    btn_connect = uicontrol('Parent', pnl_right, 'Style', 'pushbutton', 'String', 'CONNECT', ...
                            'Position', [270, 555, 120, 28], 'BackgroundColor', [0.15, 0.55, 0.30], ...
                            'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', ...
                            'Callback', @(~,~) toggle_connect());

    % Bật / Dừng Drive
    btn_power = uicontrol('Parent', pnl_right, 'Style', 'pushbutton', 'String', '⚡ SERVO ENABLED', ...
                          'Position', [15, 510, 375, 36], 'BackgroundColor', [0.15, 0.45, 0.75], ...
                          'ForegroundColor', 'w', 'FontSize', 11, 'FontWeight', 'bold', ...
                          'Callback', @(~,~) toggle_power());

    % Tabs Chọn chế độ điều khiển
    uicontrol('Parent', pnl_right, 'Style', 'text', 'String', 'OPERATING CONTROL MODE:', ...
              'Position', [15, 475, 250, 20], 'BackgroundColor', COLOR_PANEL, ...
              'ForegroundColor', [0.8, 0.85, 0.9], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    btn_mode_pos = uicontrol('Parent', pnl_right, 'Style', 'pushbutton', 'String', '🎯 POSITION', ...
                             'Position', [15, 442, 120, 30], 'BackgroundColor', COLOR_ACCENT, ...
                             'ForegroundColor', 'k', 'FontSize', 10, 'FontWeight', 'bold', ...
                             'Callback', @(~,~) set_control_mode(0));

    btn_mode_vel = uicontrol('Parent', pnl_right, 'Style', 'pushbutton', 'String', '⚡ VELOCITY', ...
                             'Position', [142, 442, 120, 30], 'BackgroundColor', COLOR_GRAY_DIM, ...
                             'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', ...
                             'Callback', @(~,~) set_control_mode(1));

    btn_mode_trq = uicontrol('Parent', pnl_right, 'Style', 'pushbutton', 'String', '⚙️ TORQUE', ...
                             'Position', [270, 442, 120, 30], 'BackgroundColor', COLOR_GRAY_DIM, ...
                             'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', ...
                             'Callback', @(~,~) set_control_mode(2));

    % =========================================================================
    % SUB-PANEL A: POSITION MODE
    % =========================================================================
    pnl_mode_pos = uipanel('Parent', pnl_right, 'Units', 'pixels', 'Position', [10, 15, 385, 415], ...
                           'BackgroundColor', [0.16, 0.18, 0.22], 'BorderType', 'none');

    uicontrol('Parent', pnl_mode_pos, 'Style', 'text', 'String', 'TARGET POSITION COMMAND (°):', ...
              'Position', [10, 385, 230, 20], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    lbl_pos_cmd = uicontrol('Parent', pnl_mode_pos, 'Style', 'text', 'String', '0.0 °', ...
                            'Position', [260, 385, 115, 20], 'BackgroundColor', [0.16, 0.18, 0.22], ...
                            'ForegroundColor', COLOR_YELLOW, 'FontSize', 11, 'FontWeight', 'bold', 'HorizontalAlignment', 'right');

    sld_pos = uicontrol('Parent', pnl_mode_pos, 'Style', 'slider', 'Min', -720, 'Max', 720, 'Value', 0, ...
                        'Position', [15, 355, 355, 22], 'Callback', @(s, ~) on_pos_slider(s.Value));

    % Presets Position
    uicontrol('Parent', pnl_mode_pos, 'Style', 'text', 'String', 'QUICK POSITION PRESETS:', ...
              'Position', [10, 315, 200, 18], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '0° (Zero)', 'Position', [10, 275, 85, 30], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_pos_command(0));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '+90°', 'Position', [102, 275, 85, 30], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_pos_command(90));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '-90°', 'Position', [194, 275, 85, 30], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_pos_command(-90));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '+180°', 'Position', [286, 275, 85, 30], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_pos_command(180));

    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '+360° (+1 Vòng)', 'Position', [10, 235, 175, 32], ...
              'BackgroundColor', [0.22, 0.26, 0.32], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_pos_command(360));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '-360° (-1 Vòng)', 'Position', [196, 235, 175, 32], ...
              'BackgroundColor', [0.22, 0.26, 0.32], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_pos_command(-360));

    % JOG Angle
    uicontrol('Parent', pnl_mode_pos, 'Style', 'text', 'String', 'JOG INCHING ANGLE:', ...
              'Position', [10, 198, 160, 18], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '◀ -10°', 'Position', [10, 165, 85, 28], ...
              'BackgroundColor', [0.30, 0.33, 0.38], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) jog_pos(-10));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '◀ -1°', 'Position', [102, 165, 85, 28], ...
              'BackgroundColor', [0.30, 0.33, 0.38], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) jog_pos(-1));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '+1° ▶', 'Position', [194, 165, 85, 28], ...
              'BackgroundColor', [0.30, 0.33, 0.38], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) jog_pos(1));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '+10° ▶', 'Position', [286, 165, 85, 28], ...
              'BackgroundColor', [0.30, 0.33, 0.38], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) jog_pos(10));

    % Max Speed
    uicontrol('Parent', pnl_mode_pos, 'Style', 'text', 'String', 'MAX PROFILE SPEED (RPM):', ...
              'Position', [10, 128, 200, 18], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '100 RPM', 'Position', [10, 95, 85, 28], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_speed_limit(100));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '300 RPM', 'Position', [102, 95, 85, 28], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_speed_limit(300));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '600 RPM', 'Position', [194, 95, 85, 28], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_speed_limit(600));
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '1000 RPM', 'Position', [286, 95, 85, 28], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_speed_limit(1000));

    % Set Home & Auto Cycle
    uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '📍 SET HOME (ZERO)', 'Position', [10, 45, 175, 36], ...
              'BackgroundColor', [0.20, 0.50, 0.45], 'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', ...
              'Callback', @(~,~) set_home_pos());
    btn_cycle = uicontrol('Parent', pnl_mode_pos, 'Style', 'pushbutton', 'String', '🔄 AUTO CYCLE (±360°)', 'Position', [196, 45, 175, 36], ...
                          'BackgroundColor', [0.30, 0.35, 0.45], 'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', ...
                          'Callback', @(~,~) toggle_auto_cycle());

    % =========================================================================
    % SUB-PANEL B: VELOCITY / SPEED MODE (MAX 1000 RPM + SNAP BRAKE)
    % =========================================================================
    pnl_mode_vel = uipanel('Parent', pnl_right, 'Units', 'pixels', 'Position', [10, 15, 385, 415], ...
                           'BackgroundColor', [0.16, 0.18, 0.22], 'BorderType', 'none', 'Visible', 'off');

    uicontrol('Parent', pnl_mode_vel, 'Style', 'text', 'String', 'TARGET SPEED COMMAND (RPM):', ...
              'Position', [10, 385, 230, 20], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    lbl_vel_cmd = uicontrol('Parent', pnl_mode_vel, 'Style', 'text', 'String', '0.0 RPM', ...
                            'Position', [260, 385, 115, 20], 'BackgroundColor', [0.16, 0.18, 0.22], ...
                            'ForegroundColor', COLOR_GREEN, 'FontSize', 11, 'FontWeight', 'bold', 'HorizontalAlignment', 'right');

    sld_vel = uicontrol('Parent', pnl_mode_vel, 'Style', 'slider', 'Min', -1000, 'Max', 1000, 'Value', 0, ...
                        'Position', [15, 355, 355, 22], 'Callback', @(s, ~) on_vel_slider(s.Value));

    % Quick Speed Presets
    uicontrol('Parent', pnl_mode_vel, 'Style', 'text', 'String', 'QUICK SPEED PRESETS (MAX 1000 RPM):', ...
              'Position', [10, 315, 260, 18], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', '150 RPM', 'Position', [10, 280, 85, 30], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_vel_command(150));
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', '300 RPM', 'Position', [102, 280, 85, 30], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_vel_command(300));
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', '600 RPM', 'Position', [194, 280, 85, 30], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_vel_command(600));
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', '1000 RPM 🚀', 'Position', [286, 280, 85, 30], ...
              'BackgroundColor', [0.15, 0.50, 0.65], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_vel_command(1000));

    % Nút DỪNG TỨC THÌ (Khựng cứng ngắc trong tích tắc)
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', '⏹ INSTANT SNAP STOP (0 RPM & KHÓA TRỤC)', ...
              'Position', [10, 228, 360, 40], 'BackgroundColor', [0.85, 0.20, 0.20], ...
              'ForegroundColor', 'y', 'FontSize', 11, 'FontWeight', 'bold', ...
              'Callback', @(~,~) send_vel_command(0));

    % JOG Run
    uicontrol('Parent', pnl_mode_vel, 'Style', 'text', 'String', 'JOG VELOCITY RUN:', ...
              'Position', [10, 192, 200, 18], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', '◀◀ CCW (-150 RPM)', 'Position', [10, 158, 175, 32], ...
              'BackgroundColor', [0.25, 0.35, 0.45], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_vel_command(-150));
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', 'CW (+150 RPM) ▶▶', 'Position', [196, 158, 175, 32], ...
              'BackgroundColor', [0.25, 0.35, 0.45], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_vel_command(150));

    % Gia tốc phanh chủ động Active Brake Deceleration
    uicontrol('Parent', pnl_mode_vel, 'Style', 'text', 'String', 'ACTIVE BRAKE RATE (GIA TỐC PHANH):', ...
              'Position', [10, 125, 260, 18], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', 'Gentle (300)', 'Position', [10, 92, 115, 28], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_decel(300));
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', 'Snap (1000) ⚡', 'Position', [132, 92, 115, 28], ...
              'BackgroundColor', [0.20, 0.45, 0.40], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_decel(1000));
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', 'Ultra (1500) 💥', 'Position', [255, 92, 115, 28], ...
              'BackgroundColor', [0.45, 0.25, 0.20], 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_decel(1500));

    % Gia tốc tăng tốc Ramp Acceleration
    uicontrol('Parent', pnl_mode_vel, 'Style', 'text', 'String', 'ACCELERATION RAMP (TĂNG TỐC):', ...
              'Position', [10, 65, 250, 18], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', 'Normal (120 rad/s²)', 'Position', [10, 32, 175, 28], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_accel(120));
    uicontrol('Parent', pnl_mode_vel, 'Style', 'pushbutton', 'String', 'Fast Ramp (250)', 'Position', [196, 32, 175, 28], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_accel(250));

    % =========================================================================
    % SUB-PANEL C: TORQUE MODE
    % =========================================================================
    pnl_mode_trq = uipanel('Parent', pnl_right, 'Units', 'pixels', 'Position', [10, 15, 385, 415], ...
                           'BackgroundColor', [0.16, 0.18, 0.22], 'BorderType', 'none', 'Visible', 'off');

    uicontrol('Parent', pnl_mode_trq, 'Style', 'text', 'String', 'TARGET TORQUE / Vq EFFORT (V):', ...
              'Position', [10, 385, 230, 20], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', 'w', 'FontSize', 10, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    lbl_trq_cmd = uicontrol('Parent', pnl_mode_trq, 'Style', 'text', 'String', '0.00 V', ...
                            'Position', [260, 385, 115, 20], 'BackgroundColor', [0.16, 0.18, 0.22], ...
                            'ForegroundColor', [0.9, 0.6, 1.0], 'FontSize', 11, 'FontWeight', 'bold', 'HorizontalAlignment', 'right');

    sld_trq = uicontrol('Parent', pnl_mode_trq, 'Style', 'slider', 'Min', -8.0, 'Max', 8.0, 'Value', 0, ...
                        'Position', [15, 355, 355, 22], 'Callback', @(s, ~) on_trq_slider(s.Value));

    uicontrol('Parent', pnl_mode_trq, 'Style', 'text', 'String', 'QUICK TORQUE EFFORT PRESETS:', ...
              'Position', [10, 315, 220, 18], 'BackgroundColor', [0.16, 0.18, 0.22], ...
              'ForegroundColor', [0.75, 0.8, 0.85], 'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');

    uicontrol('Parent', pnl_mode_trq, 'Style', 'pushbutton', 'String', '0.0 V (Free)', 'Position', [10, 275, 115, 32], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_trq_command(0.0));
    uicontrol('Parent', pnl_mode_trq, 'Style', 'pushbutton', 'String', '+2.0 V', 'Position', [132, 275, 115, 32], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_trq_command(2.0));
    uicontrol('Parent', pnl_mode_trq, 'Style', 'pushbutton', 'String', '+4.0 V', 'Position', [255, 275, 115, 32], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_trq_command(4.0));

    uicontrol('Parent', pnl_mode_trq, 'Style', 'pushbutton', 'String', '-2.0 V', 'Position', [10, 230, 115, 32], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_trq_command(-2.0));
    uicontrol('Parent', pnl_mode_trq, 'Style', 'pushbutton', 'String', '-4.0 V', 'Position', [132, 230, 115, 32], ...
              'BackgroundColor', COLOR_BTN, 'ForegroundColor', 'w', 'FontWeight', 'bold', 'Callback', @(~,~) send_trq_command(-4.0));

    % =========================================================================
    % 4. TIMERS & EVENT LOGIC
    % =========================================================================
    tmr_rx = timer('Tag', 'FOC_HMI_TIMER', 'ExecutionMode', 'fixedRate', 'Period', 0.02, ...
                   'TimerFcn', @(~,~) process_serial_stream());
    tmr_cycle = timer('Tag', 'FOC_HMI_TIMER', 'ExecutionMode', 'fixedRate', 'Period', 2.5, ...
                     'TimerFcn', @(~,~) execute_auto_cycle());
    is_cycle_running = false;
    cycle_dir = 0;

    function set_control_mode(mode_val)
        current_mode = mode_val;
        if mode_val == 0
            set(btn_mode_pos, 'BackgroundColor', COLOR_ACCENT, 'ForegroundColor', 'k');
            set(btn_mode_vel, 'BackgroundColor', COLOR_GRAY_DIM, 'ForegroundColor', 'w');
            set(btn_mode_trq, 'BackgroundColor', COLOR_GRAY_DIM, 'ForegroundColor', 'w');
            set(pnl_mode_pos, 'Visible', 'on');
            set(pnl_mode_vel, 'Visible', 'off');
            set(pnl_mode_trq, 'Visible', 'off');
            title(ax_scope, 'POSITION TRACKING TRACE (Setpoint vs Actual °)', 'Color', 'w');
            ylabel(ax_scope, 'Angle (°)', 'Color', [0.7, 0.7, 0.7]);
        elseif mode_val == 1
            set(btn_mode_pos, 'BackgroundColor', COLOR_GRAY_DIM, 'ForegroundColor', 'w');
            set(btn_mode_vel, 'BackgroundColor', COLOR_ACCENT, 'ForegroundColor', 'k');
            set(btn_mode_trq, 'BackgroundColor', COLOR_GRAY_DIM, 'ForegroundColor', 'w');
            set(pnl_mode_pos, 'Visible', 'off');
            set(pnl_mode_vel, 'Visible', 'on');
            set(pnl_mode_trq, 'Visible', 'off');
            title(ax_scope, 'VELOCITY TRACKING TRACE (Setpoint vs Actual RPM)', 'Color', 'w');
            ylabel(ax_scope, 'Velocity (RPM)', 'Color', [0.7, 0.7, 0.7]);
        else
            set(btn_mode_pos, 'BackgroundColor', COLOR_GRAY_DIM, 'ForegroundColor', 'w');
            set(btn_mode_vel, 'BackgroundColor', COLOR_GRAY_DIM, 'ForegroundColor', 'w');
            set(btn_mode_trq, 'BackgroundColor', COLOR_ACCENT, 'ForegroundColor', 'k');
            set(pnl_mode_pos, 'Visible', 'off');
            set(pnl_mode_vel, 'Visible', 'off');
            set(pnl_mode_trq, 'Visible', 'on');
            title(ax_scope, 'TORQUE / EFFORT TRACE (Vq Volts)', 'Color', 'w');
            ylabel(ax_scope, 'Vq (V)', 'Color', [0.7, 0.7, 0.7]);
        end

        if is_connected
            try writeline(s_port, sprintf('M:%d', mode_val)); catch; end
        end
    end

    function toggle_connect()
        if ~is_connected
            port_name = strtrim(edt_port.String);
            try
                s_port = serialport(port_name, 115200, 'Timeout', 0.05);
                configureTerminator(s_port, "CR/LF");
                flush(s_port);
                rx_accumulator = '';
                is_connected = true;
                set(btn_connect, 'String', 'DISCONNECT', 'BackgroundColor', COLOR_RED);
                set(lamp_ready, 'BackgroundColor', COLOR_GREEN);
                set(lamp_run, 'BackgroundColor', [0.1, 0.5, 0.9]);
                set(lamp_fault, 'BackgroundColor', COLOR_GRAY_DIM);
                start(tmr_rx);
            catch ME
                errordlg(sprintf('Không thể kết nối cổng %s:\n%s', port_name, ME.message), 'Serial Port Error');
            end
        else
            if strcmp(tmr_cycle.Running, 'on'), stop(tmr_cycle); end
            stop(tmr_rx);
            is_connected = false;
            try delete(s_port); catch; end
            s_port = [];
            set(btn_connect, 'String', 'CONNECT', 'BackgroundColor', [0.15, 0.55, 0.30]);
            set(lamp_ready, 'BackgroundColor', COLOR_GRAY_DIM);
            set(lamp_run, 'BackgroundColor', COLOR_GRAY_DIM);
            set(lamp_in_pos, 'BackgroundColor', COLOR_GRAY_DIM);
            set(lamp_at_spd, 'BackgroundColor', COLOR_GRAY_DIM);
        end
    end

    function emergency_stop()
        if is_connected
            try writeline(s_port, 'S:0'); catch; end
        end
        is_servo_on = false;
        set(btn_power, 'String', '⚠️ SERVO DISABLED (E-STOP)', 'BackgroundColor', COLOR_RED);
        set(lamp_fault, 'BackgroundColor', COLOR_RED);
        set(lamp_run, 'BackgroundColor', COLOR_GRAY_DIM);
    end

    function toggle_power()
        is_servo_on = ~is_servo_on;
        if is_servo_on
            set(btn_power, 'String', '⚡ SERVO ENABLED', 'BackgroundColor', [0.15, 0.45, 0.75]);
            set(lamp_fault, 'BackgroundColor', COLOR_GRAY_DIM);
            set(lamp_run, 'BackgroundColor', [0.1, 0.5, 0.9]);
            if is_connected, try writeline(s_port, 'S:1'); catch; end; end
        else
            set(btn_power, 'String', 'SERVO DISABLED (FREE)', 'BackgroundColor', [0.4, 0.4, 0.4]);
            set(lamp_run, 'BackgroundColor', COLOR_GRAY_DIM);
            if is_connected, try writeline(s_port, 'S:0'); catch; end; end
        end
    end

    % --- Callbacks Position Mode ---
    function on_pos_slider(val_deg)
        set(lbl_pos_cmd, 'String', sprintf('%.1f °', val_deg));
        if is_connected
            try writeline(s_port, sprintf('P:%.2f', val_deg)); catch; end
        end
    end

    function send_pos_command(val_deg)
        val_deg = max(min(val_deg, 720), -720);
        set(sld_pos, 'Value', val_deg);
        set(lbl_pos_cmd, 'String', sprintf('%.1f °', val_deg));
        if is_connected
            try writeline(s_port, sprintf('P:%.2f', val_deg)); catch; end
        end
    end

    function jog_pos(delta_deg)
        new_val = get(sld_pos, 'Value') + delta_deg;
        send_pos_command(new_val);
    end

    function send_speed_limit(rpm_val)
        if is_connected
            try writeline(s_port, sprintf('L:%.1f', rpm_val)); catch; end
        end
    end

    function set_home_pos()
        if is_connected
            try writeline(s_port, 'H:0'); catch; end
            set(sld_pos, 'Value', 0);
            set(lbl_pos_cmd, 'String', '0.0 °');
        end
    end

    function toggle_auto_cycle()
        is_cycle_running = ~is_cycle_running;
        if is_cycle_running
            set(btn_cycle, 'String', '⏹ STOP CYCLE', 'BackgroundColor', [0.8, 0.3, 0.1]);
            start(tmr_cycle);
        else
            set(btn_cycle, 'String', '🔄 AUTO CYCLE (±360°)', 'BackgroundColor', [0.30, 0.35, 0.45]);
            stop(tmr_cycle);
        end
    end

    function execute_auto_cycle()
        if is_connected
            cycle_dir = ~cycle_dir;
            if cycle_dir
                send_pos_command(360);
            else
                send_pos_command(-360);
            end
        end
    end

    % --- Callbacks Velocity Mode ---
    function on_vel_slider(val_rpm)
        set(lbl_vel_cmd, 'String', sprintf('%.1f RPM', val_rpm));
        if is_connected
            try writeline(s_port, sprintf('V:%.2f', val_rpm)); catch; end
        end
    end

    function send_vel_command(val_rpm)
        val_rpm = max(min(val_rpm, 1000), -1000);
        set(sld_vel, 'Value', val_rpm);
        set(lbl_vel_cmd, 'String', sprintf('%.1f RPM', val_rpm));
        if is_connected
            try writeline(s_port, sprintf('V:%.2f', val_rpm)); catch; end
        end
    end

    function send_accel(acc_val)
        if is_connected
            try writeline(s_port, sprintf('A:%.1f', acc_val)); catch; end
        end
    end

    function send_decel(dec_val)
        if is_connected
            try writeline(s_port, sprintf('D:%.1f', dec_val)); catch; end
        end
    end

    % --- Callbacks Torque Mode ---
    function on_trq_slider(val_vq)
        set(lbl_trq_cmd, 'String', sprintf('%.2f V', val_vq));
        if is_connected
            try writeline(s_port, sprintf('T:%.2f', val_vq)); catch; end
        end
    end

    function send_trq_command(val_vq)
        val_vq = max(min(val_vq, 8.0), -8.0);
        set(sld_trq, 'Value', val_vq);
        set(lbl_trq_cmd, 'String', sprintf('%.2f V', val_vq));
        if is_connected
            try writeline(s_port, sprintf('T:%.2f', val_vq)); catch; end
        end
    end

    % --- Telemetry Stream Processing (Non-blocking Line Buffer) ---
    function process_serial_stream()
        if is_connected && s_port.NumBytesAvailable > 0
            try
                % Đọc phi khối để không bao giờ bị nghẽn giao diện
                raw_chunk = read(s_port, s_port.NumBytesAvailable, 'char');
                rx_accumulator = [rx_accumulator, raw_chunk];

                % Tách các dòng theo ký tự xuống dòng
                lines = splitlines(rx_accumulator);
                if numel(lines) > 1
                    rx_accumulator = lines{end}; % Giữ lại đoạn chưa xong

                    % Xử lý dòng hoàn chỉnh mới nhất
                    for k = 1:(numel(lines)-1)
                        str_line = strtrim(lines{k});
                        if startsWith(str_line, "T:")
                            tokens = sscanf(str_line, 'T:%f,%f,%f,%f,%d,%d,%d');
                            if numel(tokens) == 7
                                parse_telemetry_packet(tokens);
                            end
                        end
                    end
                end
            catch
            end
        end
    end

    function parse_telemetry_packet(tokens)
        act_deg = tokens(1);
        tar_val = tokens(2);
        rpm_val = tokens(3);
        vq_val  = tokens(4);
        foc_mod = tokens(5);
        in_pos  = tokens(6);
        at_spd  = tokens(7);

        % Cập nhật Kim Tachometer
        norm_rpm = max(min(rpm_val / 1000.0, 1.0), -1.0);
        th_needle = pi/2 - norm_rpm * (3*pi/4);
        set(line_needle, 'XData', [0, 0.8*cos(th_needle)], 'YData', [0, 0.8*sin(th_needle)]);

        % Cập nhật Màn hình số 7 đoạn LED
        turns = act_deg / 360.0;
        set(lbl_act_pos, 'String', sprintf('%+.2f °  [%+.2f T]', act_deg, turns));
        set(lbl_act_vel, 'String', sprintf('%+.1f RPM  [%+.1f rad/s]', rpm_val, rpm_val * (pi / 30.0)));
        set(lbl_vq_info, 'String', sprintf('Vq: %+.2f V | Bus: 24.0 Vdc', vq_val));

        if foc_mod == 0
            set(lbl_tar_val, 'String', sprintf('%.2f °', tar_val));
        elseif foc_mod == 1
            set(lbl_tar_val, 'String', sprintf('%.1f RPM', tar_val));
        else
            set(lbl_tar_val, 'String', sprintf('%.2f V', tar_val));
        end

        % Cập nhật Pilot Lamps
        if in_pos ~= 0
            set(lamp_in_pos, 'BackgroundColor', COLOR_GREEN);
        else
            set(lamp_in_pos, 'BackgroundColor', COLOR_GRAY_DIM);
        end

        if at_spd ~= 0
            set(lamp_at_spd, 'BackgroundColor', COLOR_YELLOW);
        else
            set(lamp_at_spd, 'BackgroundColor', COLOR_GRAY_DIM);
        end

        % Cập nhật Đồ thị Scope
        if foc_mod == 0
            y_actual = [y_actual(2:end), act_deg];
            y_target = [y_target(2:end), tar_val];
        elseif foc_mod == 1
            y_actual = [y_actual(2:end), rpm_val];
            y_target = [y_target(2:end), tar_val];
        else
            y_actual = [y_actual(2:end), vq_val];
            y_target = [y_target(2:end), tar_val];
        end
        y_effort = [y_effort(2:end), vq_val];

        set(line_act, 'YData', y_actual);
        set(line_tar, 'YData', y_target);
        set(line_eff, 'YData', y_effort);

        % Auto-scale trục Y linh hoạt
        y_min = min([y_actual, y_target]);
        y_max = max([y_actual, y_target]);
        span = y_max - y_min;
        if span < 40
            mid = (y_max + y_min) / 2;
            ylim(ax_scope, [mid - 25, mid + 25]);
        else
            ylim(ax_scope, [y_min - 0.1 * span, y_max + 0.1 * span]);
        end
    end

    % Đóng ứng dụng và dọn dẹp sạch tài nguyên
    function exit_hmi()
        try
            if strcmp(tmr_cycle.Running, 'on'), stop(tmr_cycle); end
            if strcmp(tmr_rx.Running, 'on'), stop(tmr_rx); end
            delete(tmr_cycle);
            delete(tmr_rx);
        catch
        end
        if is_connected
            try
                writeline(s_port, 'S:0');
                delete(s_port);
            catch
            end
        end
        delete(fig);
    end
end
