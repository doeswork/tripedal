kinda steps!
const int STEPS_COUNT = 7;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {0, -80, 80, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, -30, -60},
  {-170, 0, 0, 0, 0, 0, 0},
  {0, 0, 0, -50, 50, 0, 0},
  {0, 40, -40, 50, -50, 0, 0},
  {0, 40, -40, 0, 0, 30, 60},
  {170, 0, 0, 0, 0, 0, 0},
};

const int STEPS_COUNT = 6;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {0, -80, 80, -50, 50, 20, 0},
  {0, 0, 0, 0, 0, 0, -40},
  {-170, 0, 0, 0, 0, -20, 0},
  {0, 40, -40, 50, -50, 0, 0},
  {0, 40, -40, 0, 0, 0, 40},
  {170, 0, 0, 0, 0, 0, 0},
};


yah! horrible walk
const int STEPS_COUNT = 7;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {0, -80, 80, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, -30, -40},
  {-180, 0, 0, 20, -20, -20, 50},
  {0, 20, -20, -20, 20, 10, -50},
  {180, 0, 0, 0, 0, 0, 0},
  {0, 20, -20, 0, 0, 30, 40},
  {0, 40, -40, 0, 0, 10, 0},
};

walk
const int STEPS_COUNT = 6;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {0, -80, 80, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, -30, -40},
  {-180, 0, 0, 20, -20, -20, 50},
  {0, 20, -20, -20, 20, 10, -50},
  {180, 10, -10, 0, 0, 10, 10},
  {0, 50, -50, 0, 0, 30, 30},
};


shorter now

//leaps but doesn't balance

const int STEPS_COUNT = 5;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {0, -80, 80, 0, 0, 10, 0},
  {-160, 0, 0, -60, 60, 0, 0},
  {0, 60, -60, 70, -70, -35, -60},
  {160, 10, -10, 30, -30, 0, 60},
  {0, 10, -10, -40, 40, 25, 0},
};

//solid crawl
const int STEPS_COUNT = 5;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {0, -80, 80, 0, 0, 40, 20},
  {0, 0, 0, 0, 0, 0, -40},
  {-160, 20, -20, -60, 60, -40, -30},
  {160, 0, 0, 0, 0, 0, 50},
  {0, 60, -60, 60, -60, 0, 0},
};

split target_pos
const int STEPS_COUNT = 6;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {0, -40, 40, -50, 50, 40, 20},
  {-160, 0, 0, -10, 10, 0, -40},
  {0, 20, -20, -20, 20, -50, -30},
  {30, 0, 0, 0, 0, 0, 0},
  {130, 0, 0, 30, -30, 10, 50},
  {0, 20, -20, 50, -50, 0, 0},
};


proper walk:
const int STEPS_COUNT = 4;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {20, 10, -10, -20, 20, -15, -30},
  {140, -20, 20, -40, 40, 15, 30}, 
  {0, 10, -10 , 60, -60, 0, 0},
  {-160, 0, 0, 0, 0, 0, 0}, 
};

First real wireless step:

const int STEPS_COUNT = 4;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {30, 0, 0, 0, 0, -30, 40}, 
  {130, -10, 10, -55, 55, 30, -40}, 
  {0, 10, -10 , 55, -55, 0, 0},
  {-160, 0, 0, 0, 0, 0, 0}, 
};


good walking
const int STEPS_COUNT = 5;
int steps[STEPS_COUNT][7] = {
  // lift, thigh, thigh, knee, knee, waist, ankle
  {30, 0, 0, 0, 0, -30, 40}, 
  {70, 0, 0, -30, 30, 15, -50}, 
  {60, -10, 10, -25, 25, 15, 0}, 
  {0, 10, -10 , 55, -55, 0, 0},
  {-160, 0, 0, 0, 0, 0, 10}, 
};