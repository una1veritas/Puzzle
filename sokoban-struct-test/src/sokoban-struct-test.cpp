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
typedef int16_t int16;
typedef unsigned int uint;

enum {
	YUKA = 1,
	WALL = 2,
	GOAL = 3,
	BOX  = 4,
	HITO = 5,
	NISE = 6,
};

struct wmap
{
	int map[640];
	int wallmap[640];
	int wid;
	int high;
};

typedef int positions[20];

struct moves
{
	positions move[100];
	positions ban[100];
	int length;
	int num;
	int banlen;
};

struct sokomap {
private:
	int width;
	int height;
	vector<int8> room;
	vector<int> places;

public:
	sokomap(const wmap & map) : width(map.wid), height(map.high) {
		int h = 0, w = 0;
		room.resize(width*height);
		places.clear();
		for(int c = 0; c < width * height; ++c) {
			h = c % width; w = c / width;
			switch (map.map[c]) {
			case WALL:
			case GOAL:
				room[c] = map.map[c];
				break;
			case BOX:
				room[c] = YUKA;
				places.push_back(c);
				break;
			case HITO:
				room[c] = YUKA;
				places[0] = c;
				break;
			default:
				room[c] = YUKA;
				break;
			}
		}
	}

	sokomap(const wmap & map, const moves & mvs) : sokomap(map) {
		arrange(mvs);
	}

	void arrange(const moves &mvs) {
		places.resize(mvs.num);
		for (int i = 0; i < places.size(); ++i)
			places[i] = mvs.move[0][i];
	}

	int8 operator()(int col, int row) const {
		int cellnum = row*width + col;
		if (room[cellnum] == WALL || room[cellnum] == GOAL)
			return room[cellnum];
		if (places[0] == cellnum)
			return HITO;
		for(int i = 1; i < places.size(); ++i) {
			if (places[i] == cellnum)
				return BOX;
		}
		return YUKA;
	}

	int cellcount() const { return height * width; }
	int boxcount() const { return places.size() - 1; }
	vector<int> & placement() { return places; }

	friend ostream & operator<<(ostream & out, const sokomap & map) {
		out << "sokomap(" << endl;
		for(int row = 0; row < map.height; ++row) {
			for(int col = 0; col < map.width; ++col) {
				switch(map(col, row)){
				case WALL:
					cout << '#';
					break;
				case HITO:
					cout << 'p';
					break;
				case BOX:
					cout << '@';
					break;
				case GOAL:
					cout << '+';
					break;
				case YUKA:
					cout << '.';
					break;
				}
			}
			cout << endl;
		}
		/*
		for(int i = 0; i < map.placement.size(); ++i) {
			cout << map.places[i] << ", ";
		}
		*/
		out << ") ";
		return out;
	}
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

	sokomap smap(mmap, mmove);
	cout << "Hello, " << endl;

	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!
	cout << smap << endl;
	//cout << smoves << endl;
	return 0;
}
