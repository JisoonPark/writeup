---
layout: post
title: horcruxes
category: Pwnable
source: "pwnable.kr"
rpath: /resource/horcruxes
tag: [rop]
---

**Category**: Pwnable

**Source**: pwnable.kr

**Points**: 7

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Voldemort concealed his splitted soul inside 7 horcruxes.  
> Find all horcruxes, and ROP it!  
> author: jiwon choi
> 
> ssh horcruxes@pwnable.kr -p2222 (pw:guest)

## Write-up

서버에 접속하여 바이너리를 실행시켜보면 7개의 horcruxes를 찾으라고 하면서 메뉴를 선택하라고 한다.

main() 함수부터 decompile 하여 차근차근 살펴보자.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // ST1C_4

  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 2, 0);
  alarm(0x3Cu);
  hint();
  init_ABCDEFG();
  v3 = seccomp_init(0);
  seccomp_rule_add(v3, 0x7FFF0000, 173, 0);
  seccomp_rule_add(v3, 0x7FFF0000, 5, 0);
  seccomp_rule_add(v3, 0x7FFF0000, 3, 0);
  seccomp_rule_add(v3, 0x7FFF0000, 4, 0);
  seccomp_rule_add(v3, 0x7FFF0000, 252, 0);
  seccomp_load(v3);
  return ropme();
}
```

alarm() 까지는 별로 볼것 없고, hint는 화면에 welcome message를 출력해주는 함수이다. seccomp를 이용해서 system call들을 필터링 하는 부분도 대충 제외하고 나면 init_ABCDEFG() 함수와 ropme() 함수가 남는다.

```c
unsigned int init_ABCDEFG()
{
  int v0; // eax
  unsigned int result; // eax
  unsigned int buf; // [esp+8h] [ebp-10h]
  int fd; // [esp+Ch] [ebp-Ch]

  fd = open("/dev/urandom", 0);
  if ( read(fd, &buf, 4u) != 4 )
  {
    puts("/dev/urandom error");
    exit(0);
  }
  close(fd);
  srand(buf);
  a = 0xDEADBEEF * rand() % 0xCAFEBABE;
  b = 0xDEADBEEF * rand() % 0xCAFEBABE;
  c = 0xDEADBEEF * rand() % 0xCAFEBABE;
  d = 0xDEADBEEF * rand() % 0xCAFEBABE;
  e = 0xDEADBEEF * rand() % 0xCAFEBABE;
  f = 0xDEADBEEF * rand() % 0xCAFEBABE;
  v0 = rand();
  g = 0xDEADBEEF * v0 % 0xCAFEBABE;
  result = f + e + d + c + b + a + 0xDEADBEEF * v0 % 0xCAFEBABE;
  sum = result;
  return result;
}
```

init_ABCDEFG 함수는 urandom에서 읽어온 값을 seed로 설정해주고 a, b, c, d, e, f, g 값을 설정 후 이들을 더해서 sum을 만드는 함수이다. 이 변수들은 모두 전역변수로 선언되어 있다.

```c
int ropme()
{
  char s[100]; // [esp+4h] [ebp-74h]
  int v2; // [esp+68h] [ebp-10h]
  int fd; // [esp+6Ch] [ebp-Ch]

  printf("Select Menu:");
  __isoc99_scanf("%d", &v2);
  getchar();
  if ( v2 == a )
  {
    A();
  }
  else if ( v2 == b )
  {
    B();
  }

  [...]

  else if ( v2 == g )
  {
    G();
  }
  else
  {
    printf("How many EXP did you earned? : ");
    gets(s);
    if ( atoi(s) == sum )
    {
      fd = open("flag", 0);
      s[read(fd, s, 0x64u)] = 0;
      puts(s);
      close(fd);
      exit(0);
    }
    puts("You'd better get more experience to kill Voldemort");
  }
  return 0;
}
```

ropme() 함수는 int 타입의 menu 값을 입력받아서 a, b, c, d, e, f, g 중 하나의 값과 동일하다면 각각 A(), B(), C(), D(), E(), F(), G() 함수를 호출하여 a, b, c, d, e,f, g의 값을 다시 출력해주고 있다.

입력한 값이 a부터 g까지의 변수들과 모두 다르다면 획득한 exp를 물어보는데, 이 값이 sum과 동일한 경우에 flag를 출력해준다.

프로그램의 동작을 찾았으니, 취약점과 공략 방법을 생각해 보자. 다행히 프로그램이 복잡하지 않아 확인할 부분이 많지는 않다.

어렵지 않게 지역변수 s에 대해 gets() 함수가 사용되어 bufffer overflow가 발생하는 것을 알 수 있다. 

![img]({{page.rpath|prepend:site.baseurl}}/checksec.png)

바이너리의 정보를 확인해 보면 canary와 PIE 모두 사용되지 않는 것으로 보이니 flag를 보여주는 부분으로 return address를 덮어써서 간단하게 해결할 수 있을 것 같다.

IDA에서 flag를 출력해주는 부분의 주소(0x80A010B)를 확인해서 return address에 덮어쓰도록 gets()에 입력값을 넣고 실행해보자.

![img]({{page.rpath|prepend:site.baseurl}}/bofres.png)

정상적으로 실행되지 않고 그냥 프로세스가 종료되어 버린다. 왜이런가 하고 자세히 봤더니, 입력으로 넣어준 주소에 0x0A가 들어있어서 gets에 입력이 들어가다가 만 것 같다.

![img]({{page.rpath|prepend:site.baseurl}}/funcaddr.png)

함수들의 주소를 잘 보면 main 함수의 끄트머리부터 0x080A0000 영역에 들어가게 된다. 역시 문제에서 주어진대로 rop를 해서 sum의 값을 알아내야 할 것 같다.

sum을 위해서는 a의 값을 알아내야 하고, a의 값을 알아내기 위해서는 A() 함수를 호출시켜야 하는데, A() 함수는 a의 값을 알아야 호출할 수 있다.

뭐 이건 정상적인 경우의 얘기고, A()부터 G() 함수의 주소들을 보면 사용하지 않아야 하는 값들이 없으므로 ropme 함수의 return address를 변조해서 A() 부터 G() 함수까지 호출되도록 해보자.

일단 return address에는 A() 함수의 값을 써주면 된다. 그럼 ropme 함수의 ret instruction이 A() 함수의 주소를 pop 하여 eip에 넣어서 A() 함수에 진입하게 해줄거고, 마찬가지로 A() 함수의 에필로그에 있는 ret instruction이 스택에서 그 다음에 있는 값을 pop 하여 eip에 넣어줄 것이다.

보통 ROP를 할 때는 호출하는 함수의 argument를 구성하기 위해 stack 구성이 좀 더 복잡해지고 pop-pop-ret 등의 가젯이 필요한데, 이 문제에서 호출할 함수들은 argument가 필요하지 않아서 그냥 A() 부터 G() 함수의 값을 스택에 순서대로 넣어주면 된다.

그렇게 하면 함수들이 순서대로 수행되면서 a부터 g의 값을 알게 되어 sum을 계산할 수 있다.

마지막으로 G() 함수의 주소 다음에 ropme()가 한번 더 실행되도록 ropme의 주소(0x0809fffc)를 넣어주면 sum을 입력한 후 flag를 확인할 수 있게 된다. (ropme()의 주소에 0x0a가 있어서, main() 함수의 마지막에 ropme를 호출하는 call instruction의 주소를 넣었다.) ([code]({{site.github.master}}{{page.rpath}}/ex.py))

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **Magic_spell_1s_4vad4_K3daVr4!**
