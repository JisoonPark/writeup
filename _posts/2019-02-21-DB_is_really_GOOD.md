---
layout: post
title: DB is really GOOD
source: "wargame.kr"
category: Web
rpath: /resource/DB_is_really_GOOD
tag: [db] 
---

**Category:** Web

**Source:** wargame.kr

**Points:** 221

**Author:** Jisoon Park(js00n.park)

**Description:** 

> What kind of this Database?
> 
> you have to find correlation between user name and database.

## Write-up

로그인을 위한 페이지가 주어지고, 로그인 해보면 메모를 입력할 수 있는 텍스트 박스와 이전에 입력했었던 히스토리가 보여진다.

텍스트박스에 이런저런 것들을 넣어봐도 딱히 되는게 없는데, 로그인을 다른 이름으로 해보면 각 id별로 메모가 별도로 관리되는 것을 알 수 있다. 아마도 db를 별도로 운영하지 않을까 하는 의심이 든다.

메모 입력 창에서는 별게 없었으니, 로그인창에 이런저런 것들을 넣어본다. **#(샵)**이나 **'(쿼트)** 같은걸 넣었을 때는 별다른 문제가 없었는데, **/(슬래시)**를 넣었더니 아래와 같은 오류가 발생했다.

![img]({{page.rpath|prepend:site.baseurl}}/error.png)

메세지를 잘 보면 db 파일을 못열어서 오류가 발생한 것을 알 수 있다.

정확한 db 이름 생성 규칙을 알기 위해 이런저런(**/a**라던가.. **a/**라던가...) 것들을 넣어보고 메세지를 살펴보면, **./db/wkrm_[id].db** 파일을 열려고 하는 것을 알 수 있다.

이거다 싶으니, **http://wargame.kr:8080/db_is_really_good/./db/wkrm_admin.db** 파일에 접근해보면, db 파일이 다운로드된다.

![img]({{page.rpath|prepend:site.baseurl}}/db.png)

db 안의 데이터를 보면 flag가 들어있는 주소를 돌려주는데, 여기에 접속해보면 flag를 얻을 수 있다.

![img]({{page.rpath|prepend:site.baseurl}}/flag.png)

Flag : **45d76a4af292fcb3a510d07ef1c46435343fc1a6**
