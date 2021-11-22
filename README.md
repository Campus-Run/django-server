# django-server


## 📜 API 명세서

| Request-Method | Request-URL | Request-Body | Success-Response-Body |
|:---:|:---:|:---:|:---:|
| **GET** | /api/init-univ | - | { status: 200, message: 'Univ table 초기화 완료' } |
| **POST** | /game/api/create-room | { title: string, creater: string, owner_univ: string, opponent_univ: string, max_join: int } | { status: 200, message: '성공적으로 Game Room을 생성하였습니다.' } |
| **POST** | /game/api/check-room-full | { roomURL: string, count: int } | { status: 200, message: "모든 참가자 참여"} |
