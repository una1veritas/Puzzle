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

class Storehouse {
private:
	vector<uint8> map;
	uint8 rows, columns;

	typedef	vector<uint16> boxplaces;
	boxplaces boxes;
	uint16 personpos;

public:
	enum {
		floor = 0,
		wall = 1,
		dest = 2,
		box = 4,
		person = 8,
	};

	Storehouse(const uint r, const uint c, const char str[]) :
	rows(r), columns(c), personpos(0) {
		for(int i = 0; str[i]; ++i) {
			switch(str[i]) {
			case '#':
				map.push_back(wall);
				break;
			case '.':
				map.push_back(floor);
				break;
			case '@':
				map.push_back(dest);
				break;
			case 'b':
			case 'B':
				map.push_back(box);
				break;
			case 'p':
			case 'P':
				map.push_back(person);
				break;
			}
		}
		if ( map.size() < r*c ) {
			cerr << "map string is not long enough." << endl;
		}
		for(uint i = 0; i < map.size(); ++i) {
			if (map[i] == box)
				boxes.push_back(i);
			if (map[i] == person)
				personpos = i;
		}
	}
};

int main() {
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!
	return 0;
}
