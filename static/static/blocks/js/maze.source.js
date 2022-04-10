/**
 * Pictures source.
 */
Maze.IDLESRC = '/static/blocks/img/idle.png';
Maze.FRONT_JUMPSRC = '/static/blocks/img/front_jump.png';
Maze.BACK_JUMPSRC = '/static/blocks/img/back_jump.png';
Maze.RIGHT_JUMPSRC = '/static/blocks/img/right_jump.png';
Maze.LEFT_JUMPSRC = '/static/blocks/img/left_jump.png';
Maze.TRUNSRC = '/static/blocks/img/turn.png';
Maze.BGSRC = '/static/blocks/img/level' + Game.LEVEL +'.jpg';
Maze.COLLECTIONSRC = '/static/blocks/img/carrot.png';

Maze.NUMSRC0 = '/static/blocks/img/number/0.png';
Maze.NUMSRC1 = '/static/blocks/img/number/1.png';
Maze.NUMSRC2 = '/static/blocks/img/number/2.png';
Maze.NUMSRC3 = '/static/blocks/img/number/3.png';
Maze.NUMSRC4 = '/static/blocks/img/number/4.png';
Maze.NUMSRC5 = '/static/blocks/img/number/5.png';
Maze.NUMSRC6 = '/static/blocks/img/number/6.png';
Maze.NUMSRC7 = '/static/blocks/img/number/7.png';
Maze.NUMSRC8 = '/static/blocks/img/number/8.png';
Maze.NUMSRC9 = '/static/blocks/img/number/9.png';

Maze.src = [Maze.IDLESRC,
Maze.FRONT_JUMPSRC,
Maze.BACK_JUMPSRC,
Maze.RIGHT_JUMPSRC,
Maze.LEFT_JUMPSRC,
Maze.TRUNSRC,
Maze.BGSRC,
Maze.COLLECTIONSRC,
Maze.NUMSRC0,
Maze.NUMSRC1,
Maze.NUMSRC2,
Maze.NUMSRC3,
Maze.NUMSRC4,
Maze.NUMSRC5,
Maze.NUMSRC6,
Maze.NUMSRC7,
Maze.NUMSRC8,
Maze.NUMSRC9];

Maze.blocks = [
	['action_forward'],
	['action_forward', 'action_turnright'],
	['action_forward', 'action_turnright', 'action_collect'],
	['action_forward', 'action_turnright', 'action_collect', 'controls_repeat'],
	['action_forward', 'action_turnright', 'action_turnleft', 'action_collect', 'controls_repeat'],
	['action_forward', 'controls_repeat', 'action_if', 'action_turnleft'],
	['action_forward', 'controls_repeat', 'action_if', 'action_turnright'],
	['action_forward', 'controls_repeat', 'action_if', 'action_turnright', 'action_turnleft'],
	['action_forward', 'controls_repeat', 'action_if', 'action_ifElse', 'action_turnright', 'action_turnleft'],
	['action_forward', 'controls_repeat', 'action_if', 'action_ifElse', 'action_turnright', 'action_turnleft']
];

Maze.maxBlocks = [undefined, // Level 0.
    Infinity, Infinity, Infinity, 6, Infinity, 4, 4, 6, 4, Infinity][Game.LEVEL];

/**
 * 1 --- path; 0 --- wall; 2 --- start; 3 --- finish.
 */
Maze.map = [
	undefined,
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  // 1
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 2, 1, 1, 3, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 2
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
	[0, 0, 0, 2, 0, 0, 3, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 3
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 4, 1, 1, 3, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 4
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 2, 0, 3, 1, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 5
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 2, 0, 0, 0, 0, 3, 0, 0],
	[0, 0, 1, 4, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 1, 4, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 1, 4, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 1, 4, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 6
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 1, 1, 3, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 2, 1, 1, 1, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 7
	[0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
	[0, 0, 2, 1, 1, 1, 1, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
	[0, 1, 1, 3, 0, 0, 0, 1, 0, 0],
	[0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  // 8
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
	[0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
	[0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
	[0, 0, 2, 1, 1, 0, 0, 3, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  // 9
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
	[0, 3, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
	[0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
	[0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 2, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
[
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  // 10
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 1, 1, 0, 0, 3, 0, 1, 0],
	[0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
	[0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
	[0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
	[0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
	[0, 0, 0, 2, 1, 1, 0, 0, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
],
][Game.LEVEL];
