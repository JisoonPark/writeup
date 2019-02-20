---
layout: post
title: Crypto Crackme Basic
category: Reversing
rpath: /resource/Crypto_Crackme_Basic
tag: [.net] 
---

**Category:** Reversing / Crypto

**Source:** wargame.kr

**Points:** 391

**Author:** Jisoon Park(js00n.park)

**Description:** 

> Simple Reverse Engineering.
> 
> Can you Reversing for C# Application?

## Write-up

.Net 기반 C# 프로그램에 대한 reversing 문제이다.

일단 JetBrains dotPeek같은 .Net decompiler를 이용해서 decompile을 시도하여 아래와 같은 코드를 얻었다.


```cs
    private static string myEncrypt(string strKey, string name)
    {
      DESCryptoServiceProvider cryptoServiceProvider = new DESCryptoServiceProvider();
      cryptoServiceProvider.Mode = CipherMode.ECB;
      cryptoServiceProvider.Padding = PaddingMode.PKCS7;
      byte[] bytes1 = Encoding.ASCII.GetBytes(Program.mPadding(name));
      cryptoServiceProvider.Key = bytes1;
      cryptoServiceProvider.IV = bytes1;
      MemoryStream memoryStream = new MemoryStream();
      CryptoStream cryptoStream = new CryptoStream((Stream) memoryStream, cryptoServiceProvider.CreateEncryptor(), CryptoStreamMode.Write);
      byte[] bytes2 = Encoding.UTF8.GetBytes(strKey.ToCharArray());
      cryptoStream.Write(bytes2, 0, bytes2.Length);
      cryptoStream.FlushFinalBlock();
      return Convert.ToBase64String(memoryStream.ToArray());
    }

    private static string mPadding(string s)
    {
      int length = s.Length;
      if (length == 8)
        return s;
      if (length > 8)
        return s.Substring(length - 8);
      for (int index = 0; index < 8 - length; ++index)
        s += "*";
      return s;
    }

    private static bool myCmp(string s1, string s2)
    {
      return s1.Length == s2.Length && !(s1 != s2);
    }

    private static void Main(string[] args)
    {
      Console.Write("Input your name : ");
      string name = Console.ReadLine();
      Console.Write("Password : ");
      string s1 = Program.myEncrypt(Console.ReadLine(), name);
      if (name == "BluSH4G" && Program.myCmp(s1, Program.getps(name)))
        Console.WriteLine("\n::Congratulation xD ::\n");
      else
        Console.WriteLine("\n:: WTF AUTH FAILED ::\n");
    }

    public static string getps(string name)
    {
      WebRequest webRequest = WebRequest.Create("http://wargame.kr:8084/prob/28/ps.php?n=" + name);
      webRequest.Credentials = CredentialCache.DefaultCredentials;
      HttpWebResponse response = (HttpWebResponse) webRequest.GetResponse();
      Stream responseStream = response.GetResponseStream();
      StreamReader streamReader = new StreamReader(responseStream);
      string end = streamReader.ReadToEnd();
      streamReader.Close();
      responseStream.Close();
      response.Close();
      return end;
    }
```

Main() 함수를 보면, name과 password를 받고, 암호화 한 후에 getps()의 결과와 비교하도록 되어있다.
if 구문으로부터 name은 **BluSH4G** 임을 쉽게 알 수 있었다.

우선, myEncrypt() 함수가 호출되는데, 내용을 보면 name에 padding을 한 것을 key로 하여 password를 DES ECB로 암호화하고 base64 encoding하도록 되어있다.

name이 뭔지 알고 있으니 mPadding() 함수를 보면 name에 "\*" 하나를 붙이는 걸로 8바이트 padding이 적용되어 key로 사용될 것을 유추할 수 있다.

getps() 함수는 name을 이용해서 서버에서 필요한 값을 받아오는데, 실제로 요청해보면 base64로 인코딩된 문자열을 돌려준다.

![img]({{page.rpath|prepend:site.baseurl}}/cipher.png)

Key를 알고 있으니, DES로 복호화 해보면 flag를 얻을 수 있다.

```python
from Crypto.Cipher import DES
import base64

obj = DES.new('BluSH4G*', DES.MODE_ECB)

cipher = base64.b64decode('7A38V6xRUofPwAj1THUFmbqNgf9CeCR7Jcp1c4F1pe/g2Bzodq7delcwt7bsML8R')

plain = obj.decrypt(cipher)
print plain
```

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : <b>c46426b4bef4ad5ec89f1f7cc6a71bde3e2bf4c2</b>
