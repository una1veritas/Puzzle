//============================================================================
// Name        : sokoban-struct-test.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <cstdint>
#include <vector>
using namespace std;

typedef int8_t int8;
typedef uint8_t uint8;
typedef uint16_t uint16;
typedef unsigned int uint;

enum {
	YUKA = 1,
	WALL = 2,
	GOAL = 3,
	BOX  = 4,
	HITO = 5,
	NISE = 6,
} map_elem;

//wmap:壁や床の位置、マップの幅を示す
struct wmap
{
	int map[640];
	int wallmap[640];
	int wid;
	int high;
};

//positions:人と箱の位置を示す
typedef int positions[20];

//moves:動きの記録
struct moves
{
	positions move[100];
	positions ban[100];
	int length;
	int num;
	int banlen;
};

int main() {

	wmap mmap = {{
	WALL,WALL,WALL,WALL,WALL,WALL,
	WALL,WALL,WALL,GOAL,GOAL,WALL,
	WALL,WALL,WALL,GOAL,GOAL,WALL,
	WALL,WALL,YUKA,YUKA,GOAL,WALL,
	WALL,YUKA,YUKA,YUKA,GOAL,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,WALL,
	WALL,WALL,YUKA,YUKA,WALL,WALL,
	WALL,WALL,WALL,WALL,WALL,WALL
	},{-1},6,11};
	moves mmove = {{{25,21,26,32,38,44,50}},{{-1}},0,7,0};

	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!
	return 0;
}
