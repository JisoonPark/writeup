---
layout: post
title: Easyhaskell
category: Reversing
rpath: /resource/Easyhaskell
tag: [base64, brute_force] 
---

**Category:** Reversing

**Source:** Samsung CTF 2017 Quals

**Points:** 150

**Author:** Kuenhwan Kwak(kh243.kwak)

**Description:** 

> Functional Language? So Easy haha:P
> 
> Flag Info : =ze=/<fQCGSNVzfDnlk$&?N3oxQp)K/CVzpznK?NeYPx0sz5

## Write-up

다운 받은 Easyhaskell 은 intel 64bit ELF executable이다. 분석에 앞서서 한번 실행해보면 Output이 출력되고 종료된다.

```
$ ./EasyHaskell
"/WGx9=ddP@f?nYp5"
```
argv 나 stdin을 해도 마찬가지 값이 출력된다.

```
$ ./EasyHaskell 1111
"/WGx9=ddP@f?nYp5"
$ ./EasyHaskell < in
"/WGx9=ddP@f?nYp5"
```
ELF 파일을 objdump 를 통해서 보면 굉장히 많은 Symbol이 검색되고 ghc를 통해서 빌드된 Haskell 로 작성한 코드임을 할 수 있다.  
확신은 없지만 <main>:0x040ad51 --> &lt;hs_main&gt;:0x047d8a0로 호출 하는 코드가 확인된다. 분석을 위해 Gdb로 hs_main 부터 Step으로 따라가 보면, &lt;rts_evalLazyIO&gt;:0x47d90b를 실행한 후부터 SIG_TRAP이 발생하면서 GDB를 사용할 수가 없게 된다. anti-debug 가 적용된 것으로 추측 된다. 

따라서 Reversing 만으로는 정확히 어떻게 결과가 나오는지 알 수없다. Decompile을해도 너무 많은 심볼이 나와서 어떤 부분이 Flag에 관련된 코드이고 어떤 부분이 Haskell에 있는 기본 심볼인지 파악이 쉽지 않다. 

종종 Windows에서 파일을 중복해서 다운받아 보면 뒤에 (1) 이 붙게 되는데 그대로 실행했다가 결과값이 바뀌는 것을 알 수 있다.

```
$ ./EasyHaskell\ \(1\)
"/WGx9=ddP@f?nYp~_2Q8"
$ ./EasyHaskell\ \(2\)
"/WGx9=ddP@f?nYp~_2;8"
```
파일명을 변경해서 실행 해보면 그에 따라서 Output 값이 변경된다.

```
$ ./a
"oH55"
$ ./aa
"oWQ5"
$ ./aaa
"oWGd"
$ ./aaaa
"oWGdoH55"
$ ./aaaaa
"oWGdoWQ5"
$ ./aaaaaa
"oWGdoWGd"
$ ./aaaaaaa
"oWGdoWGdoH55"
$ ./aaaaaaaa
"oWGdoWGdoWQ5"
$ ./aaaaaaaaa
"oWGdoWGdoWGd"
$ ./SCTF
"=ze=/~55"
```
간단한 테스트로 알수 있는 결론은
  1. 3개의 Input은 4개의 고유의 Output 을 가지며
  2. 3개 미만의 Input은 패딩을 포함해서 마찬가지로 4개의 Output이 된다.
  3. SCTF 의 문제 Flag format이 SCTF{...} 임을 감안했을때 이 값으로 넣으면 Description에 있는 Flag info의 앞 부분과 매치 된다.

따라서 EasyHaskell은 Base64 Encoding을 하는 프로그램이지만, 표준 변환 Table이 아니며 자신만의 변환 Table을 가지고 있다. 그리고 Flag info와 완전 동일한 Output을 가지게 하는 파일명이 Flag가 될 것이다.

문제를 푸는 방법은

  1. 문자열 조합을 바꿔가면서 변환 테이블을 찾고, Flag info를 Base64 Decoding을 한다.
  2. 한글자씩 맞춰서 Flag info와 4개가 맞으면 맞으면 다음 3개의 문자열을 찾는다.

2번 방식으로 풀되 가지치기를 하면서 찾으면 의외로 빠른 시간내에 답을 찾을 수 있다.

argv[0]를 바꾸는 방법은 rename으로 파일명을 바꾸는 것도 되지만 Symbolic link를 만들어도 된다.

```
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
```
run_haskell 함수는 EasyHaskell 바이너리의 Symlink를 만들어서 popen으로 실행하고 결과 값을 read 해서 return 한다. 결과값이 " "를 포함하고 있으므로 이 값은 빼준다.

```
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
...
...

```

[코드]({{site.github.master}}{{page.rpath}}/solve.c)가 다소 깔끔하진 않지만... a, b, c 가 예상 가능한 문자를 바꿔 가면서 결과 값을 확인한다.  
4개가 완전히 Match가 되는 시점에 다음 3개 문자열을 맞춘다. 그리고 Flag info와 완전 동일한 dest가 발견되면 return 한다. 
3중 for문이긴 하지만 문자열이 1개라도 같지않으면 continue로 넘어가기 때문에 생각 보다 빠른 시간 내에 답을 찾을 수 있다 


```
$$ ./solve
SCT is next
SCTF{D is next
SCTF{D0_U is next
SCTF{D0_U_KN is next
SCTF{D0_U_KNoW_ is next
SCTF{D0_U_KNoW_fUn is next
SCTF{D0_U_KNoW_fUnc10 is next
SCTF{D0_U_KNoW_fUnc10N4L is next
SCTF{D0_U_KNoW_fUnc10N4L_L4 is next
SCTF{D0_U_KNoW_fUnc10N4L_L4n9U is next
SCTF{D0_U_KNoW_fUnc10N4L_L4n9U4g3 is next
Answer : SCTF{D0_U_KNoW_fUnc10N4L_L4n9U4g3?}
```
File 명을 flag로 변경하면 description의 flag info와 동일한 출력을 확인할 수 있다.

```
$ ./SCTF\{D0_U_KNoW_fUnc10N4L_L4n9U4g3\?\}
"=ze=/<fQCGSNVzfDnlk$&?N3oxQp)K/CVzpznK?NeYPx0sz5"
```

Flag : **SCTF{D0_U_KNoW_fUnc10N4L_L4n9U4g3?}**
