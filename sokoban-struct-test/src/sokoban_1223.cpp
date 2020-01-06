#include <stdio.h>
#include <time.h>
#include <algorithm>
#include <vector>
#define YUKA 1
#define WALL 2
#define GOAL 3
#define BOX  4
#define HITO 5
#define NISE 6

using namespace std;

//wmap:壁や床の位置、マップの幅を示す
typedef struct
{
	int map[640];
	int wallmap[640];
	int wid;
	int high;
} wmap;

//positions:人と箱の位置を示す

typedef int positions[20];

bool positions_equals(const positions &p, const positions &it, const int num)
{
	int i;
	for (i = 1; i < num; ++i)
	{
		if (it[i] != p[i])
			break;
	}
	return i == num;
};

//moves:動きの記録
struct moves
{
	positions move[100];
	positions ban[100];
	int length;
	int num;
	int banlen;
};

typedef struct
{
	int spot;
	int cost;
} ableach;

typedef struct
{
	ableach area[300];
} ablea;

typedef struct
{
	int boxn;
	int around[4];
} boxsit;

typedef struct
{
	boxsit sits[20];
	int numbox;
} solids;

int solver(wmap *, moves *);
int isLoop(wmap *, moves *);
int isBan(wmap *, moves *);
int isTumi(wmap *, moves *);
int whatThere(wmap *, moves *, int);
int whatBan(wmap *, moves *, int);
int isClear(wmap *, moves *);
int advance(wmap *, moves *, int);
int isReach(wmap *, moves *, int);
int isPassed(ablea *, int);
int canMove(wmap *, moves *, int);
int tumibox(solids *, int, int *);
int lowSearch(int *, int, int);
int addBan(moves *);
int isStop(wmap *, int);
int isClosed(wmap *, moves *);
int isNTW(wmap *, int);
void admitBan(wmap *);
void oneBack(moves *);
void printMap(wmap *, moves *);
void printMove(moves *);
void printAblea(ablea *);
void finRoute(wmap *, moves *);

long int q = 0;
int dirs[4];

void admitBan(wmap *amap)
{
	int i, k = 0, sdir;
	for (i = 0; i < amap->wid * amap->high; i++)
	{
		amap->wallmap[i] = amap->map[i];
		if (amap->map[i] == YUKA)
		{
			if (isNTW(amap, i))
			{
				amap->wallmap[i] = NISE;
			}
			
		}
	}
}

int isNTW(wmap *nmap, int posi)
{
	int sdir, k = 1, dir, flag = 1;
	for (sdir = 0; sdir < 4; sdir++)
	{
		if (nmap->map[posi + dirs[sdir]] == WALL)
		{
			dir = dirs[(sdir + 1) % 4];
			while (nmap->map[posi + k * dir] != WALL)
			{
				if (nmap->map[posi + (k * dir) + dirs[sdir]] != WALL)
				{
					flag = 0;
				}
				if (nmap->map[posi + (k * dir)] == GOAL)
				{
					flag = 0;
				}
				k++;
			}
			k = 1;

			dir = dirs[(sdir + 3) % 4];
			while (nmap->map[posi + k * dir] != WALL)
			{
				if (nmap->map[posi + (k * dir) + dirs[sdir]] != WALL)
				{
					flag = 0;
				}
				if (nmap->map[posi + (k * dir)] == GOAL)
				{
					flag = 0;
				}
				k++;
			}
			k = 1;
			if (flag)
			{
				return 1;
			}
			flag = 1;
		}
	}
	return 0;
}

//通ったか調べる
int isPassed(ablea *parea, int plook)
{
	int i = 0;
	//printAblea(parea);
	while (parea->area[i].spot != -1)
	{
		if (parea->area[i].spot == plook)
		{
			return 1;
		}
		i++;
	}

	return 0;
}

//到達可能か調べる
int isReach(wmap *lmap, moves *lmove, int posi)
{
	int i = 0, j = 1, something, looking;

	if (lmove->move[lmove->length][0] == posi)
	{
		return 0;
	}

	ablea rarea;
	rarea.area[0].spot = lmove->move[lmove->length][0];
	rarea.area[0].cost = 0;
	rarea.area[1].spot = -1;
	rarea.area[1].cost = -1;

	//printAblea(&rarea);

	while (rarea.area[i].spot != -1)
	{
		//上を見る
		looking = rarea.area[i].spot - lmap->wid;
		//何か見て床ゴールで未到達だったら収納
		something = whatThere(lmap, lmove, looking);
		if (something == YUKA || something == GOAL)
		{
			if (looking == posi)
			{
				return rarea.area[i].cost + 1;
			}
			if (!isPassed(&rarea, looking))
			{
				rarea.area[j].spot = looking;
				rarea.area[j].cost = rarea.area[i].cost + 1;
				rarea.area[j + 1].spot = -1;
				j++;
			}
		}

		//下
		looking = rarea.area[i].spot + lmap->wid;
		something = whatThere(lmap, lmove, looking);
		if (something == YUKA || something == GOAL)
		{
			if (looking == posi)
			{
				return rarea.area[i].cost + 1;
			}
			if (!isPassed(&rarea, looking))
			{
				rarea.area[j].spot = looking;
				rarea.area[j].cost = rarea.area[i].cost + 1;
				rarea.area[j + 1].spot = -1;
				j++;
			}
		}

		//左
		looking = rarea.area[i].spot - 1;
		something = whatThere(lmap, lmove, looking);
		if (something == YUKA || something == GOAL)
		{
			if (looking == posi)
			{
				return rarea.area[i].cost + 1;
			}
			if (!isPassed(&rarea, looking))
			{
				rarea.area[j].spot = looking;
				rarea.area[j].cost = rarea.area[i].cost + 1;
				rarea.area[j + 1].spot = -1;
				j++;
			}
		}

		//右
		looking = rarea.area[i].spot + 1;
		something = whatThere(lmap, lmove, looking);
		if (something == YUKA || something == GOAL)
		{
			if (looking == posi)
			{
				return rarea.area[i].cost + 1;
			}
			if (!isPassed(&rarea, looking))
			{
				rarea.area[j].spot = looking;
				rarea.area[j].cost = rarea.area[i].cost + 1;
				rarea.area[j + 1].spot = -1;
				j++;
			}
		}

		i++;
	}
	return -1;
}

//進めたら進む
int advance(wmap *amap, moves *amove, int dir)
{
	int i, k = 0, something, behbox, boxnum, posi;
	posi = amove->move[amove->length][0];
	something = whatThere(amap, amove, posi + dir);

	if (something == YUKA || something == GOAL)
	{
		for (i = 0; i < amove->num; i++)
		{
			amove->move[amove->length + 1][i] = amove->move[amove->length][i];
		}
		amove->move[amove->length + 1][0] += dir;
		amove->length++;
		return 1;
	}

	if (something == BOX)
	{
		behbox = whatThere(amap, amove, posi + (2 * dir));
		if (behbox == YUKA || behbox == GOAL)
		{
			if(amap->wallmap[posi + (2*dir)] != NISE){
				for (i = 0; i < amove->num; i++)
				{
					amove->move[amove->length + 1][i] = amove->move[amove->length][i];
					if (amove->move[amove->length][i] == amove->move[amove->length][0] + dir)
					{
						amove->move[amove->length + 1][i] += dir;
					}
				}
				amove->move[amove->length + 1][0] += dir;
				amove->length++;
                if(behbox == GOAL){
                    if(isStop(amap,posi + (2*dir))){
						if(isClosed(amap,amove)){
							//printf("aaa\n");
							amove->length--;
							amap->wallmap[posi + (2*dir)] = GOAL;
							return 0;
						}
						return 2;
					}
                }
				return 1;
			}
		}
	}
	return 0;
}

int isStop(wmap *cmap, int posi){
    int sdir,flag=0b00;
    for (sdir = 0; sdir < 4; sdir++)
	{
		if (cmap->wallmap[posi + dirs[sdir]] == WALL)
		{
			if (sdir % 2 == 0)
			{
				flag = flag | 0b10;
			}
			else
			{
				flag = flag | 0b01;
			}
		}
    }

    if(flag == 0b11){
        cmap->wallmap[posi] = WALL;
        return 1;
    }
    return 0;
}

int isClosed(wmap *cmap, moves *cmove){
	
	int i = 0, j = 1, something, looking, sdir, goalnum=0;

	ablea rarea;
	rarea.area[0].spot = cmove->move[cmove->length][0];
	rarea.area[0].cost = 0;
	rarea.area[1].spot = -1;
	rarea.area[1].cost = -1;

	//printAblea(&rarea);

	while (rarea.area[i].spot != -1)
	{
		if(cmap->map[rarea.area[i].spot] == GOAL){
			goalnum++;
		}
		if(cmap->wallmap[rarea.area[i].spot] != WALL){
			for(sdir=0; sdir<4; sdir++)
			{
				looking = rarea.area[i].spot + dirs[sdir];
				something = cmap->map[looking];
				if (something == YUKA || something == GOAL)
				{
					//printf("%d is %d\n", looking, something);
					if (!isPassed(&rarea, looking))
					{
						rarea.area[j].spot = looking;
						rarea.area[j].cost = rarea.area[i].cost + 1;
						rarea.area[j + 1].spot = -1;
						j++;
					}
				}
			}
			if(goalnum == cmove->num-1)
			{
				return 0;
			}
		}
		i++;
	}
	//printf("%d",i);
	return 1;
}



//クリアしてるかチェック
int isClear(wmap *cmap, moves *cmove)
{
	int i;
	for (i = 1; i < cmove->num; i++)
	{
		if (cmap->map[cmove->move[cmove->length][i]] != GOAL)
		{
			return 0;
		}
	}
	return 1;
}

//ループしてないかチェック
int isLoop(wmap *lmap, moves *lmove)
{
	int i, flag;
	if (lmove->length != 0)
	{
		for (i = 0; i < lmove->length; i++)
		{
			flag = 1;
			if (isReach(lmap, lmove, lmove->move[i][0]) == -1)
			{
				flag = 0;
			}
			else if (!positions_equals(lmove->move[i], lmove->move[lmove->length], lmove->num))
			{
				flag = 0;
			}

			if (flag == 1)
			{
				return 1;
			}
		}
	}

	return 0;
}

int isBan(wmap *lmap, moves *lmove)
{
	int i, flag;
	if (lmove->banlen != 0)
	{
		for (i = 0; i < lmove->banlen; i++)
		{
			flag = 1;
			if (isReach(lmap, lmove, lmove->ban[i][0]) == -1)
			{
				//printf("notreach\n");
				flag = 0;
			}
			else if (!positions_equals(lmove->ban[i], lmove->move[lmove->length], lmove->num))
			{
				flag = 0;
			}

			if (flag == 1)
			{
				//printf("it's ban\n\n");
				return 1;
			}
		}
	}
	//printf("it's new\n\n");
	return 0;
}

int addBan(moves *bmove)
{
	int i;
	if (bmove->banlen < 100)
	{
		for (i = 0; i < bmove->num; i++)
		{
			bmove->ban[bmove->banlen][i] = bmove->move[bmove->length][i];
		}
		bmove->banlen++;
	}
	else
	{
		return 0;
	}
	return 1;
}

//積んでないかチェック
int isTumi(wmap *tmap, moves *tmove)
{
	int i, flag = 0b00, bflag = 0b00, something, somes[4] = {YUKA, YUKA, YUKA, YUKA}, posi, bp = 0;
	solids boxlow;
	boxlow.numbox = 0;
	for (i = 1; i < tmove->num; i++)
	{
		posi = tmove->move[tmove->length][i];
		something = whatThere(tmap, tmove, posi - tmap->wid);
		if (something == WALL)
		{
			flag = flag | 0b10;
		}
		if (something == BOX)
		{
			bflag = bflag | 0b10;
		}
		somes[0] = something;

		something = whatThere(tmap, tmove, posi + tmap->wid);
		if (something == WALL)
		{
			flag = flag | 0b10;
		}
		if (something == BOX)
		{
			bflag = bflag | 0b10;
		}
		somes[2] = something;

		something = whatThere(tmap, tmove, posi - 1);
		if (something == WALL)
		{
			flag = flag | 0b01;
		}
		if (something == BOX)
		{
			bflag = bflag | 0b01;
		}
		somes[1] = something;

		something = whatThere(tmap, tmove, posi + 1);
		if (something == WALL)
		{
			flag = flag | 0b01;
		}
		if (something == BOX)
		{
			bflag = bflag | 0b01;
		}
		somes[3] = something;

		if (flag == 0b11)
		{
			if (tmap->map[posi] != GOAL)
			{
				return 1;
			}
		}

		flag = flag | bflag;
		if (flag == 0b11)
		{
			int k;
			boxlow.sits[bp].boxn = posi;
			boxlow.numbox++;
			for (k = 0; k < 4; k++)
			{
				if (somes[k] != YUKA)
				{
					boxlow.sits[bp].around[k] = somes[k];
				}
				else
				{
					boxlow.sits[bp].around[k] = YUKA;
				}
			}
			bp++;
		}
		flag = 0b00;
		bflag = 0b00;
	}
	int j, l;
	//for(l=0; l<bp; l++){
	//printf("%d ", boxlow.sits[l].boxn);
	//}
	//printf("\n\n");
	for (j = 0; j < bp; j++)
	{
		int looked[20] = {boxlow.sits[j].boxn, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
		if (tumibox(&boxlow, j, looked))
		{
			//printf("goal?\n");
			if (tmap->map[boxlow.sits[j].boxn] != GOAL)
			{
				return 1;
			}
		}
	}
	return 0;
}

int tumibox(solids *tboxlow, int bp, int looked[])
{
	int i, j, tflag = 0b00, look, k = 0;

	for (i = 0; i < 4; i++)
	{
		if (tboxlow->sits[bp].around[i] == WALL)
		{
			if (i % 2 == 0)
			{
				tflag = tflag | 0b10;
			}
			else
			{
				tflag = tflag | 0b01;
			}
		}
		if (tboxlow->sits[bp].around[i] == BOX)
		{
			look = tboxlow->sits[bp].boxn + dirs[i];
			for (j = 0; j <= tboxlow->numbox; j++)
			{
				if (tboxlow->sits[j].boxn == look)
				{
					if (lowSearch(looked, look, 20) == -1)
					{
						if (tumibox(tboxlow, j, looked))
						{
							if (i % 2 == 0)
							{
								tflag = tflag | 0b10;
							}
							else
							{
								tflag = tflag | 0b01;
							}
						}
					}
					else
					{
						if (i % 2 == 0)
						{
							tflag = tflag | 0b10;
						}
						else
						{
							tflag = tflag | 0b01;
						}
					}
				}
			}
		}
	}
	if (tflag == 0b11)
	{
		return 1;
	}
	return 0;
}

int lowSearch(int low[], int tar, int end)
{
	int i;
	for (i = 0; i < end; i++)
	{
		if (low[i] == tar)
		{
			return i;
		}
		if (low[i] == -1)
		{
			low[i] = tar;
			break;
		}
	}
	return -1;
}

//何があるか
int whatThere(wmap *whmap, moves *whmove, int posi)
{
	int i;

	if (whmap->map[posi] != WALL)
	{
		if (whmove->move[whmove->length][0] == posi)
		{
			return HITO;
		}
		for (i = 1; i < whmove->num; i++)
		{
			if (whmove->move[whmove->length][i] == posi)
			{
				return BOX;
			}
		}
	}
	if (whmap->wallmap[posi] == NISE){
        return YUKA;
    }

	return whmap->wallmap[posi];
}

int whatBan(wmap *whmap, moves *whmove, int posi)
{
	int i;
	if (whmap->map[posi] != WALL)
	{
		if (whmove->ban[whmove->banlen][0] == posi)
		{
			return HITO;
		}
		for (i = 1; i < whmove->num; i++)
		{
			if (whmove->ban[whmove->banlen][i] == posi)
			{
				return BOX;
			}
		}
	}

	return whmap->map[posi];
}

//人を移動する
int canMove(wmap *mmap, moves *mmove, int posi)
{

	if (mmove->move[mmove->length][0] == posi)
	{
		return 1;
	}
	int i, cost = isReach(mmap, mmove, posi);
	if (cost != -1)
	{
		for (i = 1; i < mmove->num; i++)
		{
			mmove->move[mmove->length + 1][i] = mmove->move[mmove->length][i];
		}
		mmove->move[mmove->length + 1][0] = posi;
		mmove->length++;
		//printf("%d\n", posi);
		return 1;
	}
	return 0;
}

void oneBack(moves *bmove)
{
	bmove->length--;
}

void printMap(wmap *pmap, moves *pmove)
{
	int i, something;
	for (i = 0; i < (pmap->high * pmap->wid); i++)
	{
		something = whatThere(pmap, pmove, i);
		//something = whatBan(pmap,pmove,i);

		if (something == YUKA)
		{
			printf(" ");
		}
		else if (something == WALL)
		{
			printf("#");
		}
		else if (something == BOX)
		{
			if (pmap->map[i] == GOAL)
			{
				printf("0");
			}
			else
			{
				printf("O");
			}
		}
		else if (something == HITO)
		{
			printf("@");
		}
		else if (something == GOAL)
		{
			printf("X");
		}
		else
		{
			printf("%d", something);
		}
		if ((i + 1) % pmap->wid == 0)
		{
			printf("\n");
		}
	}
	printf("\n");
}

void finRoute(wmap *fmap, moves *fmove)
{
	int len, stu;
	stu = fmove->length;
	//stu = fmove->banlen;
	for (len = 0; len <= stu; len++)
	{
		fmove->length = len;
		//fmove->banlen = len;
		printMap(fmap, fmove);
		while (getchar() != '\n')
			;
	}
}

void printMove(moves *pmove)
{
	int i, j;
	for (i = 0; i <= pmove->length; i++)
	{
		for (j = 0; j < pmove->num; j++)
		{
			printf("%d ", pmove->move[i][j]);
		}
		printf("\n");
	}
	printf("\n");
}

void printAblea(ablea *parea)
{
	int i = 0;
	while (parea->area[i].spot != -1)
	{
		printf("%d", parea->area[i].spot);
		i++;
	}
	printf("\n");
}

//ソルバー関数本体
int solver(wmap *smap, moves *smove)
{
	std::sort(smove->move[smove->length]+1, smove->move[smove->length] + smove->num);
	q++;
	//int hero = q;
	if (q % 10000 == 0)
	{
		//printf("%d\n", q);
		printMap(smap, smove);
		//printMove(smove);
		//printf("%d\n", smove->length);
		//while(getchar() != '\n');
	}
	//std::sort(smove->move[smove->length]+1, smove->move[smove->length] + smove->num);

	if (smove->length == 99)
	{
		//printf("max\n");
		return -1;
	}

	if (isLoop(smap, smove))
	{
		//if(q>100000){
		//printf("loop\n");
		//}
		return 0;
	}

	if (isBan(smap, smove))
	{
		//printf("ban\n");
		return 0;
	}

	if (isClear(smap, smove))
	{
		//printf("clear\n");
		return 1;
	}

	if (isTumi(smap, smove))
	{
		//if(q>100000){
		//printf("tumi\n");
		//}
		return 0;
	}

	//printMap(smap,smove);
	//while(getchar() != '\n');

	int i, sdir, len = smove->length, solflag, advflag, cloflag=0,maxflag=0;
	for (i = 1; i < smove->num; i++)
	{
		for (sdir = 0; sdir < 4; sdir++)
		{
			if (canMove(smap, smove, smove->move[smove->length][i] + dirs[sdir]))
			{
				advflag = advance(smap, smove, -dirs[sdir]);
				
				if(advflag != 0)
				{
					solflag = solver(smap,smove);
					if (solflag == 1)
					{
						return 1;
					}
					else if(solflag == -1){
						maxflag = 0;
					}
					oneBack(smove);
				}
				if (smove->length != len)
				{
					oneBack(smove);
				}
				if(advflag == 2){
					//printf("oooo\n");
					smap->wallmap[smove->move[smove->length][i] - dirs[sdir]] = GOAL;
				}
			}
		}
	}

	//printf("end\n");
	if(maxflag){
		return -1;
	}

	if (!isBan(smap, smove))
	{
		//printf("hero is %d\n",hero);
		//printMap(smap,smove);
		//while(getchar() != '\n');
		if (!addBan(smove))
		{
			//printf("max\n");
			//finRoute(smap,smove);
		}
	}

	return 0;
}

//メイン
int main(void)
{
	int m;
	clock_t t1, t2;

	/*
	wmap mmap = {{
	WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,
	WALL,GOAL,YUKA,YUKA,YUKA,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,YUKA,YUKA,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,YUKA,YUKA,YUKA,YUKA,WALL,
	WALL,GOAL,YUKA,YUKA,YUKA,YUKA,YUKA,WALL,
	WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL
	},8,6};
	moves mmove = {{{20,12,27,35}},0,4};
	*/

	/*
	wmap mmap = {{
	WALL,WALL,WALL,WALL,WALL,
	WALL,GOAL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,
	WALL,WALL,WALL,WALL,WALL
	},5,5};
	moves mmove = {{{17,12}},{{-1}},0,2,0};
	*/

	/*
	wmap mmap = {{
	WALL,WALL,WALL,WALL,WALL,WALL,WALL,
	WALL,WALL,WALL,WALL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,YUKA,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,WALL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,WALL,YUKA,WALL,WALL,
	WALL,WALL,YUKA,WALL,YUKA,YUKA,WALL,
	WALL,WALL,YUKA,GOAL,YUKA,YUKA,WALL,
	WALL,WALL,WALL,WALL,WALL,WALL,WALL
	},7,8};
	moves mmove = {{{18,23}},{-1},0,2,0};
	*/

	/*
	wmap mmap = {{
	WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL,
	WALL, WALL, GOAL, YUKA, GOAL, WALL, WALL, WALL,
	WALL, WALL, WALL, GOAL, YUKA, WALL, WALL, WALL,
	WALL, YUKA, YUKA, YUKA, YUKA, YUKA, YUKA, WALL,
	WALL, GOAL, YUKA, YUKA, YUKA, YUKA, YUKA, WALL,
	WALL, WALL, WALL, YUKA, YUKA, YUKA, YUKA, WALL,
	WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL
	},{-1},8,7};
	moves mmove = {{{43, 35, 26, 28, 11}}, {{-1}}, 0, 5, 0};
	*/

	/*
	wmap mmap = {{
	WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,
	WALL,WALL,GOAL,YUKA,GOAL,WALL,WALL,WALL,
	WALL,WALL,WALL,GOAL,YUKA,WALL,WALL,WALL,
	WALL,YUKA,YUKA,YUKA,YUKA,YUKA,YUKA,WALL,
	WALL,GOAL,YUKA,YUKA,YUKA,YUKA,YUKA,WALL,
	WALL,WALL,WALL,YUKA,YUKA,YUKA,YUKA,WALL,
	WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL
	},8,7};
	moves mmove = {{{25,24,19,20,11}},0,5};
	*/

	/*
	wmap mmap = {{
	WALL,WALL,WALL,WALL,WALL,WALL,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,YUKA,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,YUKA,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,YUKA,WALL,
	WALL,WALL,WALL,WALL,WALL,WALL,WALL
	},7,5};
	moves mmove = {{{16,19}},0,2};
	*/

	/*
	wmap mmap = {{
	WALL,WALL,WALL,WALL,WALL,
	WALL,YUKA,YUKA,GOAL,WALL,
	WALL,YUKA,YUKA,YUKA,WALL,
	WALL,GOAL,YUKA,YUKA,WALL,
	WALL,WALL,WALL,WALL,WALL
	},5,5};
	moves mmove = {{{7,12,17}},0,3};
	*/

	/*
	wmap mmap = {{
	WALL,WALL,WALL,WALL,
	WALL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,WALL,
	WALL,GOAL,WALL,WALL,
	WALL,GOAL,WALL,WALL,
	WALL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,WALL,
	WALL,YUKA,YUKA,WALL,
	WALL,WALL,WALL,WALL
	},4,12};
	moves mmove = {{{13,17,37}},{-1},0,3,0};
	*/

	
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
	

	dirs[0] = -mmap.wid;
	dirs[1] = -1;
	dirs[2] = mmap.wid;
	dirs[3] = 1;

	//std::sort(mmove.move[0]+1, mmove.move[0] + mmove.num);
	admitBan(&mmap);
	/*
	int k=0;
	while(mmap.banarea[k]!=-1){
		printf("%d ",mmap.banarea[k]);
		k++;
	}
	printf("\n");
	*/

	t1 = clock();
	printf("%d\n", solver(&mmap, &mmove));
	t2 = clock();
	printf("%fSECOND\n", (double)(t2 - t1) / CLOCKS_PER_SEC);
	printf("%ldPOINT\n", q);
	finRoute(&mmap, &mmove);
	return 0;
}
