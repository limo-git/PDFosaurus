# Configuration
PX_SIZE = 15  
GRID_WIDTH = 60
GRID_HEIGHT = 20  
GRID_OFF_X = 100
GRID_OFF_Y = 300

PDF_FILE_TEMPLATE = """
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages 2 0 R
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

2 0 obj
<<
  /Count 1
  /Kids [
    16 0 R
  ]
  /Type /Pages
>>

%% Annots Page 1 (also used as overall fields list)
21 0 obj
[
  ###FIELD_LIST###
]
endobj

###FIELDS###

%% Page 1
16 0 obj
<<
  /Annots 21 0 R
  /Contents 3 0 R
  /CropBox [
    0.0
    0.0
    900.0  
    900.0  
  ]
  /MediaBox [
    0.0
    0.0
    900.0  
    900.0  
  ]
  /Parent 2 0 R
  /Resources <<
  >>
  /Rotate 0
  /Type /Page
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj


42 0 obj
<< >>
stream

function createInterval(cb, ms) {
    var evalStr = "(" + cb.toString() + ")();";
    return app.setInterval(evalStr, ms);
}

// Game constants
var TICK_INTERVAL = 50;
var INITIAL_GAME_SPEED = 700; 
var GAME_SPEED = INITIAL_GAME_SPEED;
var JUMP_HEIGHT = 8;  
var MIN_GAME_SPEED = 200; 
var JUMP_DISTANCE = 6; 

// Obstacle types
var OBSTACLE_TYPES = [
    { type: "small", width: 1, height: 2 },
    { type: "medium", width: 2, height: 3 },
    { type: "tall", width: 1, height:5 },  
    { type: "wide", width: 2, height: 2 },  
    { type: "large", width: 2, height: 4 }  
];

// Cloud patterns 
var CLOUD_PATTERNS = [
    { pattern: "~~~~", width: 4 },
    { pattern: "~~~", width: 3 },
    { pattern: "~~~~~", width: 5 },
    { pattern: "~~~~~~", width: 6 }  
];

// Game variables
var pixel_fields = [];
var score = 0;
var game_running = false;
var interval_id = null;

// Objects
var dino_x = 3;
var dino_y = 1; 
var dino_jumping = false;
var jump_counter = 0;
var jump_distance_traveled = 0;

var obstacles = [];
var clouds = [];
var time_counter = 0;
var obstacle_timer = 0;
var cloud_timer = 0;
var difficulty_level = 1;

function initialize_game() {
    console.println("Initializing game...");
    
    // Get references to all pixel fields
    for (var x = 0; x < ###GRID_WIDTH###; ++x) {
        pixel_fields[x] = [];
        for (var y = 0; y < ###GRID_HEIGHT###; ++y) {
            var field_name = "P_" + x + "_" + y;
            pixel_fields[x][y] = this.getField(field_name);
        }
    }
    
    reset_game();
    game_running = true;
    
    this.getField("B_start").hidden = true;
    this.getField("B_jump").hidden = false;
    this.getField("B_restart").hidden = true;
    
    
    interval_id = createInterval(game_loop, TICK_INTERVAL);
    console.println("Game started with interval ID: " + interval_id);
}

function reset_game() {
    console.println("Resetting game...");
    score = 0;
    obstacles = [];
    clouds = [];
    dino_y = 1; 
    dino_jumping = false;
    jump_counter = 0;
    jump_distance_traveled = 0;
    time_counter = 0;
    obstacle_timer = 150; 
    cloud_timer = 50; 
    difficulty_level = 1;
    GAME_SPEED = INITIAL_GAME_SPEED; 
    
    
    clear_screen();
    
    
    draw_ground();
    
    
    create_initial_clouds();
    
    
    this.getField("T_score").value = "Score: 0";
    this.getField("T_level").value = "Level: 1";
}

function create_initial_clouds() {

    for (var i = 0; i < 5; i++) {  
        var cloudPattern = CLOUD_PATTERNS[Math.floor(Math.random() * CLOUD_PATTERNS.length)];
        clouds.push({
            x: 10 + Math.floor(Math.random() * (###GRID_WIDTH### - 20)),
            y: 15 + Math.floor(Math.random() * 8), 
            pattern: cloudPattern.pattern,
            width: cloudPattern.width
        });
    }
}

function game_loop() {
    if (!game_running) return;
    
    time_counter++;
    
    
    clear_screen();
    draw_ground();
    
    // Handle jumping 
    if (dino_jumping) {
        jump_counter++;
        
        var totalJumpFrames = JUMP_DISTANCE * (GAME_SPEED/100);
        var jumpPeakFrames = totalJumpFrames * 0.4; 
        var jumpFallFrames = totalJumpFrames * 0.6; 
        
        if (jump_counter < jumpPeakFrames) {
            
            dino_y = 1 + Math.min(JUMP_HEIGHT, Math.floor((jump_counter / jumpPeakFrames) * JUMP_HEIGHT));
        } else if (jump_counter <= totalJumpFrames) {
            
            var fallProgress = (jump_counter - jumpPeakFrames) / jumpFallFrames;
            dino_y = JUMP_HEIGHT + 1 - Math.min(JUMP_HEIGHT, Math.floor(fallProgress * JUMP_HEIGHT));
            
            
            if (jump_counter >= totalJumpFrames) {
                dino_y = 1;
                dino_jumping = false;
                jump_counter = 0;
                jump_distance_traveled = 0;
            }
        }
    }
    
    
    cloud_timer--;
    if (cloud_timer <= 0) {
        
        var cloudPatternIndex = Math.floor(Math.random() * CLOUD_PATTERNS.length);
        var cloudPattern = CLOUD_PATTERNS[cloudPatternIndex];
        
        clouds.push({
            x: ###GRID_WIDTH### - 1,
            y: 10 + Math.floor(Math.random() * 8), 
            pattern: cloudPattern.pattern,
            width: cloudPattern.width
        });
        
        
        cloud_timer = 150 + Math.floor(Math.random() * 100);
    }
    
    
    if (time_counter % Math.floor(GAME_SPEED/50) === 0) {
        for (var i = clouds.length - 1; i >= 0; i--) {
            clouds[i].x--;
            
            
            if (clouds[i].x + clouds[i].width < 0) {
                clouds.splice(i, 1);
            }
        }
    }
    
    
    for (var i = 0; i < clouds.length; i++) {
        draw_cloud(clouds[i]);
    }
    
    
    draw_dino();
    
    
    obstacle_timer--;
    if (obstacle_timer <= 0) {
        
        var obstacleIndex = Math.floor(Math.random() * OBSTACLE_TYPES.length);
        if (difficulty_level > 3) {
            obstacleIndex = Math.min(obstacleIndex + 1, OBSTACLE_TYPES.length - 1);
        }
        var obstacleType = OBSTACLE_TYPES[obstacleIndex];
        
        obstacles.push({
            x: ###GRID_WIDTH### - 1,
            width: obstacleType.width,
            height: obstacleType.height,
            type: obstacleType.type
        });
        
        
        var baseTimer = 120 - (difficulty_level * 10);
        obstacle_timer = Math.max(50, baseTimer) + Math.floor(Math.random() * 30);
    }
    
    
    if (time_counter % Math.floor(GAME_SPEED/100) === 0) {
        
        for (var i = obstacles.length - 1; i >= 0; i--) {
            obstacles[i].x--;
            
            if (obstacles[i].x + obstacles[i].width < 0) {
                obstacles.splice(i, 1);
                score++;
                this.getField("T_score").value = "Score: " + score;
                
                
                if (score % 5 === 0) {
                    increase_difficulty();
                }
            }
        }
    }
    
    for (var i = 0; i < obstacles.length; i++) {
        draw_obstacle(obstacles[i]);
        
        if (check_collision(obstacles[i])) {
            game_over();
        }
    }
}

function increase_difficulty() {
    if (GAME_SPEED > MIN_GAME_SPEED) {
        GAME_SPEED -= 35 + difficulty_level * 5; 
        GAME_SPEED = Math.max(GAME_SPEED, MIN_GAME_SPEED); 
    }
    
    if (score % 10 === 0) {
        difficulty_level++;
        this.getField("T_level").value = "Level: " + difficulty_level;
    }
}

function jump() {
    if (!dino_jumping && game_running) {
        dino_jumping = true;
        jump_counter = 0;
        jump_distance_traveled = 0;
    }
}

function game_over() {
    console.println("Game over!");
    game_running = false;
    
    if (interval_id !== null) {
        app.clearInterval(interval_id);
        interval_id = null;
    }
    
    app.alert("Game Over! Your score: " + score + " (Level " + difficulty_level + ")\\nClick Restart to play again.");
    
    this.getField("B_jump").hidden = true;
    this.getField("B_restart").hidden = false;
}

function restart_game() {
    console.println("Restarting game...");
    
    if (interval_id !== null) {
        app.clearInterval(interval_id);
    }
    
    reset_game();
    game_running = true;
    
    this.getField("B_restart").hidden = true;
    this.getField("B_jump").hidden = false;
    
    interval_id = createInterval(game_loop, TICK_INTERVAL);
}

function check_collision(obstacle) {
    if (dino_x < obstacle.x + obstacle.width && 
        dino_x + 1 > obstacle.x && 
        dino_y < obstacle.height + 1) { 
        return true;
    }
    return false;
}

function draw_pixel(x, y, visible) {
    if (x < 0 || y < 0 || x >= ###GRID_WIDTH### || y >= ###GRID_HEIGHT###) {
        return;
    }
    
    pixel_fields[x][y].hidden = !visible;
}

function draw_text(x, y, text) {
    var pixels = create_text_pixels(x, y, text);
    for (var i = 0; i < pixels.length; i++) {
        draw_pixel(pixels[i].x, pixels[i].y, true);
    }
}

function create_text_pixels(x, y, text) {
    var pixels = [];
    for (var i = 0; i < text.length; i++) {
        pixels.push({x: x + i, y: y});
    }
    return pixels;
}

function clear_screen() {
    for (var x = 0; x < ###GRID_WIDTH###; x++) {
        for (var y = 0; y < ###GRID_HEIGHT###; y++) {
            draw_pixel(x, y, false);
        }
    }
}

function draw_ground() {
    for (var x = 0; x < ###GRID_WIDTH###; x++) {
        draw_pixel(x, 0, true);
    }
}

function draw_dino() {
    draw_pixel(dino_x, dino_y, true);     
    draw_pixel(dino_x, dino_y + 1, true); 
    draw_pixel(dino_x, dino_y + 2, true); 
    draw_pixel(dino_x, dino_y + 3, true); 
}

function draw_obstacle(obstacle) {
    for (var x = 0; x < obstacle.width; x++) {
        for (var y = 0; y < obstacle.height; y++) {
            draw_pixel(obstacle.x + x, y + 1, true);
        }
    }
}

function draw_cloud(cloud) {
    draw_text(cloud.x, cloud.y, cloud.pattern);
}

function handle_keydown(event) {
    if (event.keyCode === 32 || 
        event.keyCode === 38) { 
        jump();
    }
}


try {
    this.addKeyHandler({
        onKeyDown: handle_keydown
    });
} catch (e) {
    console.println("Could not add key handler: " + e);
}

console.println("Script loaded successfully");


app.execMenuItem("FitPage");

endstream
endobj


18 0 obj
<<
  /JS 43 0 R
  /S /JavaScript
>>
endobj


43 0 obj
<< >>
stream



endstream
endobj

trailer
<<
  /Root 1 0 R
>>

%%EOF
"""

PLAYING_FIELD_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      0.9 0.9 0.9
    ]
    /BC [
      0 0 0
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (playing_field)
  /Type /Annot
>>
endobj
"""

PIXEL_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      ###COLOR###
    ]
    /BC [
      0.2 0.2 0.2
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_AP_STREAM = """
###IDX### obj
<<
  /BBox [ 0.0 0.0 ###WIDTH### ###HEIGHT### ]
  /FormType 1
  /Matrix [ 1.0 0.0 0.0 1.0 0.0 0.0]
  /Resources <<
    /Font <<
      /HeBo 10 0 R
    >>
    /ProcSet [ /PDF /Text ]
  >>
  /Subtype /Form
  /Type /XObject
>>
stream
q
0.75 g
0 0 ###WIDTH### ###HEIGHT### re
f
Q
q
1 1 ###WIDTH### ###HEIGHT### re
W
n
BT
/HeBo 12 Tf
0 g
10 8 Td
(###TEXT###) Tj
ET
Q
endstream
endobj
"""

BUTTON_OBJ = """
###IDX### obj
<<
  /A <<
	  /JS ###SCRIPT_IDX### R
	  /S /JavaScript
	>>
  /AP <<
    /N ###AP_IDX### R
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      0.75
    ]
    /CA (###LABEL###)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

TEXT_OBJ = """
###IDX### obj
<<
	/F 4
	/FT /Tx
	/MK <<
	>>
	/MaxLen 0
	/P 16 0 R
	/Rect [
		###RECT###
	]
	/Subtype /Widget
	/T (###NAME###)
	/V (###LABEL###)
	/Type /Annot
>>
endobj
"""

STREAM_OBJ = """
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""

fields_text = ""
field_indexes = []
obj_idx_ctr = 50

def add_field(field):
    global fields_text, field_indexes, obj_idx_ctr
    fields_text += field
    field_indexes.append(obj_idx_ctr)
    obj_idx_ctr += 1

# Playing field outline
playing_field = PLAYING_FIELD_OBJ
playing_field = playing_field.replace("###IDX###", f"{obj_idx_ctr} 0")
playing_field = playing_field.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y} {GRID_OFF_X+GRID_WIDTH*PX_SIZE} {GRID_OFF_Y+GRID_HEIGHT*PX_SIZE}")
add_field(playing_field)

# Create pixel fields
for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        # We'll use y=0 for the ground at the bottom
        pixel = PIXEL_OBJ
        pixel = pixel.replace("###IDX###", f"{obj_idx_ctr} 0")
        pixel = pixel.replace("###COLOR###", "0.1 0.1 0.1")
        pixel = pixel.replace("###RECT###", f"{GRID_OFF_X + x * PX_SIZE} {GRID_OFF_Y + y * PX_SIZE} {GRID_OFF_X + x * PX_SIZE + PX_SIZE} {GRID_OFF_Y + y * PX_SIZE + PX_SIZE}")
        pixel = pixel.replace("###X###", f"{x}")
        pixel = pixel.replace("###Y###", f"{y}")
        add_field(pixel)

def add_button(label, name, x, y, width, height, js):
    script = STREAM_OBJ
    script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
    script = script.replace("###CONTENT###", js)
    add_field(script)

    ap_stream = BUTTON_AP_STREAM
    ap_stream = ap_stream.replace("###IDX###", f"{obj_idx_ctr} 0")
    ap_stream = ap_stream.replace("###TEXT###", label)
    ap_stream = ap_stream.replace("###WIDTH###", f"{width}")
    ap_stream = ap_stream.replace("###HEIGHT###", f"{height}")
    add_field(ap_stream)

    button = BUTTON_OBJ
    button = button.replace("###IDX###", f"{obj_idx_ctr} 0")
    button = button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-2} 0")
    button = button.replace("###AP_IDX###", f"{obj_idx_ctr-1} 0")
    button = button.replace("###NAME###", name)
    button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(button)

def add_text(label, name, x, y, width, height):
    text = TEXT_OBJ
    text = text.replace("###IDX###", f"{obj_idx_ctr} 0")
    text = text.replace("###LABEL###", label)
    text = text.replace("###NAME###", name)
    text = text.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(text)

# Add buttons
add_button("Start Game", "B_start", GRID_OFF_X + GRID_WIDTH*PX_SIZE/2 - 75, GRID_OFF_Y + GRID_HEIGHT*PX_SIZE/2 - 25, 150, 50, "initialize_game();")
add_button("Jump", "B_jump", GRID_OFF_X, GRID_OFF_Y - 70, 100, 50, "jump();")
add_button("Restart", "B_restart", GRID_OFF_X, GRID_OFF_Y - 70, 100, 50, "restart_game();")

# Initially hide controls
script = STREAM_OBJ
script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
script = script.replace("###CONTENT###", "this.getField('B_jump').hidden = true; this.getField('B_restart').hidden = true;")
add_field(script)

# Add score display
add_text("Score: 0", "T_score", GRID_OFF_X, GRID_OFF_Y + GRID_HEIGHT*PX_SIZE + 20, 150, 30)
# Add level display
add_text("Level: 1", "T_level", GRID_OFF_X + 200, GRID_OFF_Y + GRID_HEIGHT*PX_SIZE + 20, 150, 30)

# Create PDF
filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))
filled_pdf = filled_pdf.replace("###GRID_WIDTH###", f"{GRID_WIDTH}")
filled_pdf = filled_pdf.replace("###GRID_HEIGHT###", f"{GRID_HEIGHT}")

pdffile = open("dinosaur_game.pdf", "w")
pdffile.write(filled_pdf)
pdffile.close()
