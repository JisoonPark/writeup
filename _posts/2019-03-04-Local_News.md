---
layout: post
title: Local News
category: Reversing
source: "TAMUctf 2019"
rpath: /resource/Local_News
tag: [apk]
---

**Category**: Reversing/Android

**Source**: TAMUctf 2019

**Points**: 478

**Author**: Jisoon Park(js00n.park)

**Description:** 

> Be sure to check your local news broadcast for the latest updates!
> 
> Difficulty: medium-hard
> 
> [app.apk]({{site.github.master}}{{page.rpath}}/app.apk)

## Write-up

우선 jadx-gui를 사용해 MainActivity를 살펴보자.

```Java
public class MainActivity extends AppCompatActivity {
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView((int) R.layout.activity_main);
        BroadcastReceiver hidden = new BroadcastReceiver() {
            public void onReceive(Context context, Intent intent) {
                Log.d(MainActivity.this.getString(R.string.flag), Deobfuscator$app$Debug.getString(0));
            }
        };
        IntentFilter filter = new IntentFilter();
        filter.addAction(getString(R.string.hidden_action));
        LocalBroadcastManager.getInstance(this).registerReceiver(hidden, filter);
    }
}
```
BroadcastReceiver를 만들어서 OnReceive() 함수를 정의하는데, 뭔가 broadcast가 들어오면 Deobfuscator 클래스의 getString(0) 메소를 호출해서 그 결과를 로그로 출력하고 있다. 해당 클래스를 따라가보자.

Deobfuscator 클래스에는 getString() 메소드 하나 밖에 없다. 일단 에뮬레이터에 앱을 올린 후 브로드캐스트를 날려 보는 것도 방법이겠지만, 귀찮으니 그냥 아래와 같이 코드를 복사해서 돌려보았다.

```java
public class HelloWorld{
    private static final String[] charChunks = new String[]{"}18m_hanbed3i{0g"};
    private static final String[] indexChunks = new String[]{"\u000f\f\u000f\t\u0003\r\u0005\f\n\n\t\u0007\u0004\u0002\u0001\u0006\t\b\u000e\u0001\u000b\b\t\u0006\u0000"};
    private static final String[] locationChunks = new String[]{"\u0000\u0000\u0019\u0000"};

    public static final int USER_MASK = 65535;

    public static String getString(int id) {
        int location1Index = id % 4096;
        int location2ChunkIndex = (id + 1) / 4096;
        int location2Index = (id + 1) % 4096;
        String locations1 = locationChunks[id / 4096];
        String locations2 = locationChunks[location2ChunkIndex];
        int offset1 = ((locations1.charAt((location1Index * 2) + 1) & USER_MASK) << 16) | (locations1.charAt(location1Index * 2) & USER_MASK);
        int length = ((locations2.charAt((location2Index * 2) + 1) << 16) | locations2.charAt(location2Index * 2)) - offset1;
        char[] stringChars = new char[length];
        for (int i = 0; i < length; i++) {
            int offset = offset1 + i;
            int indexIndex = offset % 8192;
            int index = indexChunks[offset / 8192].charAt(indexIndex) & USER_MASK;
            int charIndex = index % 8192;
            stringChars[i] = charChunks[index / 8192].charAt(charIndex);
        }
        return new String(stringChars);
    }

     public static void main(String []args){
        System.out.println(getString(0));
     }
}
```

중간에 **SupportMenu.USER_MASK**라는 변수를 사용하는데, 이 변수는 **import android.support.v4.internal.view.SupportMenu;** 구문을 따라 가보면 65535임을 쉽게 확인할 수 있다.

위 코드를 실행해보면 바로 flag를 확인할 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **gigem{hidden_81aeb013bea}**
