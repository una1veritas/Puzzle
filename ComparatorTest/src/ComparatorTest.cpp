//============================================================================
// Name        : ComparatorTest.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <vector>
#include <set>

using namespace std;

struct cmp {
	static int base;

	static void set_base(int x) { base = x; }

	bool operator()(const int a, const int b) const {
		return (a % base) < (b % base);
	}
};
int cmp::base = 111;

int main() {
	set<int, cmp> a_set;
	cmp::set_base(4);

	int a[] = { 1, 2, 6, 7, 9, 12, 13, 15, 0};
	for(int i = 0; a[i]; ++i)
		a_set.insert(a[i]);

	for(auto i : a_set)
		cout << i << ", ";
	cout << std::endl;
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!
	return 0;
}
