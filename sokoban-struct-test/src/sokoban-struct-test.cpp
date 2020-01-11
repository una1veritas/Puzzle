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

typedef unsigned int uint;
typedef int8_t int8;

enum {
	YUKA = 1,
	WALL = 2,
	GOAL = 3,
	BOX  = 4,
	HITO = 5,
	NISE = 6,
};

struct _wmap
{
	int map[640];
	int wallmap[640];
	int wid;
	int high;
};

typedef int _positions[20];

struct _moves
{
	_positions move[100];
	_positions ban[100];
	int length;
	int num;
	int banlen;
};

struct sokomap {
private:
	int width;
	int height;
	vector<int8> wallmap;
	vector<int> positions;

public:
	sokomap(const _wmap & map) : width(map.wid), height(map.high) {
		int h = 0, w = 0;
		wallmap.resize(width*height);
		positions.clear();
		for(int c = 0; c < width * height; ++c) {
			h = c % width; w = c / width;
			switch (map.map[c]) {
			case WALL:
			case GOAL:
				wallmap[c] = map.map[c];
				break;
			case BOX:
				wallmap[c] = YUKA;
				positions.push_back(c);
				break;
			case HITO:
				wallmap[c] = YUKA;
				positions[0] = c;
				break;
			default:
				wallmap[c] = YUKA;
				break;
			}
		}
	}

	sokomap(const _wmap & map, const _moves & mvs) : sokomap(map) {
		place(mvs);
	}

	sokomap(const char mapstr[]) {
		int c, r;
		for( c = 0; mapstr[c]; ++c) {
			if ( mapstr[c] == '\n' )
				break;
		}
		width = c;
		positions.push_back(0);
		const char * p = mapstr;
		for (r = 0; ; ++r) {
			++height;
			for(c = 0; c < width; ++c) {
				switch(*p++) {
				case '#':
					wallmap.push_back(WALL);
					break;
				case '.':
					wallmap.push_back(YUKA);
					break;
				case '+':
					wallmap.push_back(GOAL);
					break;
				case '@':
					wallmap.push_back(YUKA);
					positions.push_back(width * r + c);
					break;
				case 'p':
					wallmap.push_back(YUKA);
					positions[0] = width * r + c;
					break;
				}
			}
			if ( isspace(*p) )
				p++; // skip '\n'
			if ( *p == 0 ) {
				break;
			}
		}
	}

	void place(const _moves &mvs) {
		positions.resize(mvs.num);
		for (int i = 0; i < positions.size(); ++i)
			positions[i] = mvs.move[0][i];
		std::sort(positions.begin() + 1, positions.end());
	}

	int8 operator()(int col, int row) const {
		int cellnum = row*width + col;
		if (wallmap[cellnum] == WALL || wallmap[cellnum] == GOAL)
			return wallmap[cellnum];
		if (positions[0] == cellnum)
			return HITO;
		for(int i = 1; i < positions.size(); ++i) {
			if (positions[i] == cellnum)
				return BOX;
		}
		return YUKA;
	}

	int cellcount() const { return height * width; }
	int boxcount() const { return positions.size() - 1; }
	vector<int> & placement() { return positions; }

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

struct sokomoves {
	sokomap & smap;
	vector<vector<int> > placements;

public:
	sokomoves(sokomap & map) : smap(map) {
		placements.push_back(smap.placement());
	}

	sokomoves(sokomap & map, const _moves & mov) : smap(map) {
		placements.push_back(vector<int>(mov.num));
		for(int i = 0; i < mov.num; ++i)
			placements.back()[i] = mov.move[0][i];
	}

	const vector<int> & operator[](const int & i) const {
		return placements[i];
	}

	int boxcount() const { return smap.boxcount(); }
	int person() const { return placements.back().front(); }
	vector<int> & placement() { return placements.back(); }

	friend ostream & operator<<(ostream & out, const sokomoves & moves) {
		for(int v = 0; v < moves.placements.size(); ++v) {
			out << "[";
			out << moves[v][0] << "; ";
			for(int i = 1; i < moves[v].size(); ++i) {
				out << moves[v][i] << ", ";
			}
			out << "], ";
		}
		return out;
	}
};

int main() {

	_wmap mmap = {{
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
	_moves mmove = {{{25,21,26,32,38,44,50}},{{-1}},0,7,0};

	sokomap smap(mmap, mmove);
	sokomoves mymoves(smap, mmove), bannedmoves(smap);
	sokomap map2(
			"######\n"
			"###++#\n"
			"###++#\n"
			"##.@+#\n"
			"#p@.+#\n"
			"#.@.##\n"
			"#.@.##\n"
			"#.@.##\n"
			"#.@.##\n"
			"##..##\n"
			"######");

	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!
	cout << smap << endl;
	cout << mymoves << endl;
	cout << endl << endl;
	cout << map2 << endl;

	return 0;
}
