#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>

char src[] = "./EasyHaskell";
char goal[] = "=ze=/<fQCGSNVzfDnlk$&?N3oxQp)K/CVzpznK?NeYPx0sz5";
char dest[NAME_MAX] = {0,};
char cdest[NAME_MAX] = {0,};
char string[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890+._=-{}?";

int dest_cur = 0;
int goal_cur = 0;

char* run_haskell(char *in)
{
	char path[NAME_MAX]; 
	char buf[1024];
	int len;
	FILE *fp;
	symlink(src, in);
	snprintf(path, NAME_MAX, "./%s", in);
	fp = popen(path, "r");
	if( fp == NULL ){
		unlink(in);
		return NULL;
	}

	fgets(buf, 1024, fp);
	unlink(in);
	fclose(fp);
	len = strlen(buf);
	buf[len-2] = 0;
	return strdup(buf+1);
}

int main(void)
{
	int a,b,c;
	char next[4] = {0,};
	FILE *fp;
	char buf[1024];
	char *answer_a;
	char *answer_b;
	char *answer_c;
	int size = sizeof(string);

again:
		for(a = 0 ;a < size; a++) {
			next[0] = string[a];
			dest[dest_cur] = string[a];
			answer_a = run_haskell(dest);
			if( answer_a == NULL ) {
				continue;
			}
			if( strcmp(goal, answer_a) == 0){
				printf ("Answer : %s\n", dest);
				return 0;
			}
			if( answer_a[goal_cur] == goal[goal_cur] )
			{
				for(b = 0; b < size ; b++){
					next[1] = string[b];
					dest[dest_cur + 1] = string[b];
					answer_b = run_haskell(dest);
					if( answer_b == NULL ) {
						continue;
					} 
					if( answer_b[goal_cur+1] == goal[goal_cur+1] )
					{
						if( strcmp(goal, answer_b) == 0){
							printf ("Answer : %s\n", dest);
							return 0;
						}
						for(c = 0 ; c < size ; c++) {
							next[2] = string[c];
							dest[dest_cur+2] = string[c];
							answer_c = run_haskell(dest);
							if( answer_c == NULL ) {
								continue;
							}

							if( strcmp(goal, answer_c) == 0){
								printf ("Answer : %s\n", dest);
								return 0;
							}
							if( strncmp(goal, answer_c, goal_cur+4) == 0) {
								free(answer_a);
								free(answer_b);
								free(answer_c);
								goto match;
							}
							free(answer_c);
						}
					}
					free(answer_b);
				}
			}
			free(answer_a);
		}
match:
		printf("%s is next\n", dest);
		dest[dest_cur] = next[0];
		dest[dest_cur+1] = next[1];
		dest[dest_cur+2] = next[2];
		dest[dest_cur+3] = 0;
		goal_cur += 4;
		dest_cur += 3;
		memset(next, 0, 4);
goto again;
}
