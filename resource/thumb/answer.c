
#include<stdio.h>
#include<stdint.h>

unsigned char map[16][16];

unsigned char final[16][16] = {{0x3f, 0xb1, 0xbf, 0x52, 0x98, 0x88, 0x35, 0x9d, 0x29, 0x3d, 0xa8, 0x49, 0xa2, 0xa8, 0x4b, 0xc3},
						  {0xeb, 0x68, 0x26, 0xce, 0x0d, 0x49, 0xfe, 0x08, 0xcd, 0x25, 0x73, 0x64, 0x4e, 0x78, 0xf5, 0xea},
						  {0x17, 0x56, 0xdd, 0xee, 0x2f, 0x4c, 0xc6, 0x0b, 0x9c, 0x05, 0x40, 0x8e, 0x77, 0x24, 0xf4, 0x02},
						  {0xB7, 0x0C, 0xD2, 0xAD, 0xED, 0x08, 0x18, 0x2A, 0xCA, 0xEE, 0xD4, 0x2A, 0x72, 0xA6, 0x13, 0xC6},
						  {0x58, 0xF5, 0x7C, 0x27, 0xAC, 0x81, 0x0F, 0x13, 0xC7, 0x14, 0x4E, 0xA7, 0x8C, 0x51, 0x09, 0x8A},
						  {0xDE, 0x02, 0x14, 0x7E, 0x9D, 0x8E, 0xDC, 0x68, 0x22, 0x77, 0x14, 0xC4, 0xF8, 0xC2, 0xC4, 0x66},
						  {0xBF, 0x09, 0x23, 0x2F, 0xD2, 0x8D, 0xDD, 0x7F, 0xA0, 0xA3, 0x89, 0x47, 0xE6, 0x04, 0x6B, 0xFC},
						  {0x87, 0x32, 0x48, 0x0D, 0xAC, 0x59, 0x9F, 0x0D, 0xDD, 0xCF, 0x2F, 0x60, 0xC3, 0x3D, 0x36, 0xCB},
						  {0x23, 0xB6, 0x00, 0x54, 0x91, 0x5A, 0xC5, 0x4A, 0x7C, 0x93, 0xDF, 0xFE, 0xF5, 0x1E, 0x63, 0xD4},
						  {0x6E, 0x9D, 0x9B, 0x85, 0x63, 0x44, 0xFC, 0xA3, 0xE3, 0x00, 0xD4, 0x22, 0xB5, 0xDA, 0xDB, 0x7E},
						  {0x1D, 0x26, 0x44, 0x5E, 0x12, 0x58, 0x39, 0x84, 0x6A, 0x7B, 0x2C, 0xB3, 0x4C, 0x45, 0x13, 0x1F},
						  {0xBB, 0x2D, 0xDF, 0x95, 0xC3, 0xF4, 0x03, 0x7D, 0x6E, 0xB4, 0xB5, 0xCC, 0xB7, 0xEA, 0x0F, 0x59},
						  {0xCC, 0xED, 0x6B, 0x40, 0x43, 0x7C, 0x51, 0x79, 0x84, 0x25, 0x9A, 0x4C, 0xC0, 0x78, 0x0A, 0xBF},
						  {0xF6, 0x2F, 0x55, 0x8D, 0x99, 0x6A, 0x4B, 0x33, 0xBC, 0xEB, 0x1E, 0x91, 0x6B, 0x52, 0x32, 0x0D},
						  {0xFD, 0x8A, 0x7C, 0x94, 0x5F, 0x01, 0x2B, 0xC8, 0xA9, 0xA8, 0xB1, 0xA0, 0x00, 0x20, 0x50, 0x1F},
						  {0x6A, 0x6E, 0x2F, 0x46, 0xF6, 0x15, 0x23, 0x94, 0x57, 0xD2, 0x56, 0x9C, 0x9C, 0x4B, 0x51, 0xBD}};



#define N 624
#define M 397
#define MATRIX_A 0x9908b0df   /* constant vector a */
#define UPPER_MASK 0x80000000 /* most significant w-r bits */
#define LOWER_MASK 0x7fffffff /* least significant r bits */

/* Tempering parameters */   
#define TEMPERING_MASK_B 0x9d2c5680
#define TEMPERING_MASK_C 0xefc60000
#define TEMPERING_SHIFT_U(y)  (y >> 11)
#define TEMPERING_SHIFT_S(y)  (y << 7)
#define TEMPERING_SHIFT_T(y)  (y << 15)
#define TEMPERING_SHIFT_L(y)  (y >> 18)

static unsigned long mt[N]; /* the array for the state vector  */
static int mti=N+1; /* mti==N+1 means mt[N] is not initialized */

void init_seed(unsigned long seed)
{
	mt[0]= seed & 0xffffffff;
	for (mti=1; mti<N; mti++)
		mt[mti] = (uint32_t)(0x6c078965 * (mt[mti-1]^(mt[mti-1] >>30)) +mti);
}

unsigned long mt_rand()
{
	unsigned long y;
	static unsigned long mag01[2]={0x0, MATRIX_A};
	/* mag01[x] = x * MATRIX_A  for x=0,1 */

	if (mti >= N) { /* generate N words at one time */
		int kk;

		if (mti == N+1)   /* if sgenrand() has not been called, */
			init_seed(0xC0FFEE); /* a default initial seed is used   */

		for (kk=0;kk<N-M;kk++) {
			y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
			mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1];
		}
		for (;kk<N-1;kk++) {
			y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
			mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1];
		}
		y = (mt[N-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);
		mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1];

		mti = 0;
	}

	y = mt[mti++];
	y ^= TEMPERING_SHIFT_U(y);
	y ^= TEMPERING_SHIFT_S(y) & TEMPERING_MASK_B;
	y ^= TEMPERING_SHIFT_T(y) & TEMPERING_MASK_C;
	y ^= TEMPERING_SHIFT_L(y);

	return y;
}

char INPUT[] = "SCTFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";

void input_string(char ch, int num)
{
	char c;
	int i;
	unsigned char a;
	unsigned char b;


	for(i = 0 ; i < 34 ; i++)
	{
		c = INPUT[i];
		if( num == i ) {
			c = ch;
		}
		a = (mt_rand()&0xF);
		b = (mt_rand()&0xF);
		map[a][b] = (unsigned char)(map[a][b]^c);
	}
}

void init_map(void)
{
	int i, j;
	unsigned char val;
	unsigned long rand;

	for(i = 0 ; i < 16 ; i++)
	{
		for(j = 0 ; j < 16 ; j++)
		{
			rand = mt_rand();
			val = (unsigned char)rand;
			map[i][j] = val;
		}
	}
}


void dump_map(unsigned char arr[][16])
{
	int i, j;
	for(i = 0 ; i < 16 ; i++)
	{
		for(j =0 ; j < 16 ; j++)
		{
			printf("[%02X]", arr[i][j]);
		}
		printf("\n");
	}

}

void swap1(int a, int b)
{
	unsigned char tmp;
	int i;

	for(i = 0 ; i < 16 ; i++)
	{		
		tmp = map[i][a];
		map[i][a] = map[i][b];
		map[i][b] = tmp;
	}
}

void rshift(int a, char b)
{
	int i;
	unsigned char right = 0;
	unsigned char left;

	right = 0;
	for(i =0 ; i < 16 ; i++)
	{
		left = (uint8_t)(map[a][i]&((1<<b)-1))<<(8-b);
		map[a][i] = right | (map[a][i] >> b);
		right = left;

	}
	map[a][0] |= right; 
}

void eor(int a, int b, uint32_t c)
{
	int i;

	for(i = 0 ; i < 16 ; i++)
	{
		map[i][b] = (unsigned char)map[i][b]^c;
		map[a][i] = (unsigned char)map[a][i]^c;
	}
}

void swap2(int a, int b)
{
	unsigned char tmp;
	int i;

	for(i = 0 ; i < 16 ; i++)
	{		
		tmp = map[a][i];
		map[a][i] = map[b][i];
		map[b][i] = tmp;
	}
}

int main(void)
{
	int i, j, k, l;
	int cnt;
	int c;
	int idx = 0;
	int max_cnt;
	char max_ch;


	int next;

	for(idx = 4; idx < 34 ; idx++)
	{
		max_cnt = 0;
		max_ch = ' ';
		for( c = 32 ; c < 127 ; c++)
		{
			init_seed(0xC0FFEE);

			init_map();
			input_string(c,idx);

			for(i = 0 ; i < 1000 ; i++)
			{
				int a;
				int b;
				a = mt_rand()&0xF;
				b = mt_rand()&0xF;
				swap2(a, b);
			}


			for(j = 0 ; j < 1000 ; j++)
			{
				int a;
				char b;

				a = mt_rand()&0xF;
				b = mt_rand()&0x7;
				rshift(a, b);
			}

			for(k = 0 ; k < 1000 ; k++)
			{
				int a;
				int b;
				uint32_t c;

				a = mt_rand()&0xF;
				b = mt_rand()&0xF;
				c = mt_rand();
				eor(a, b, c);
			}

			for(l = 0 ; l < 1000 ; l++)
			{
				int a;
				int b;
				a = mt_rand()&0xF;
				b = mt_rand()&0xF;
				swap1(a, b);
			}

			cnt = 0;
			for(i = 0 ; i < 16 ; i++)
			{
				for(j = 0 ; j < 16 ; j++)
				{
					if(map[i][j] == final[i][j])
						cnt++;
				}
			}
			if(max_cnt < cnt) {
				max_cnt = cnt;
				max_ch = c;
				INPUT[idx] = max_ch;
			} 
		}
		printf("%s\n", INPUT);
	}
}

