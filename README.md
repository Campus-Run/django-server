# 🏫 Campus-Run
> Campus-Run is a 3D racing game set on a college campus. <br>
> Designed this service to comfort university students who are unable to visit the campus in person due to the COVID-19. <br>
> Providing various ways(text and video chat) to communicate with people from different universities <br>
> **Enjoy your sprint!** and never miss the chance to socialize with people without a mask 😷.

<div align="center">
  
  <img src="https://user-images.githubusercontent.com/39653584/145571114-c7575006-488f-403b-baef-c3a617708308.jpeg" width="800px" height="500px">
  <br />  <br />
  
  [🎖 **Capstone-Design Contest**🎖](http://www.swaicau.com/bbs/board.php?bo_table=program8&wr_id=38) <br />
  [🎬 **DEMO Video**🎬](https://www.youtube.com/watch?v=cRBCqWESeLI&t=5s)<br />  <br />
</div>

---

# 🕹 Django-Server
> You can check the node-server [here.](https://github.com/youngkwon02/CampusRun-node-server)<br/>
> Django-Server is used to access and manage the database. <br>
> We've implemented various data-accessing APIs like below. <br>
<br>

### ⭐️ User and univ related
| Request-Method | Request-URI | About | Written-By |
|:---:|:---:|:---:|:---:|
| **POST** | /api/user | Get user data using user's token | [<img src="https://avatars.githubusercontent.com/u/49235528?s=70&v=4" width="30px">](https://github.com/oereo) | 
| **POST** | /api/init-univ | Supporting university data initializing | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /login/kakao/callback | Kakao social sign-in when user inputs are correct | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /activate/<str:uidb64>/<str:token> | Univ e-mail authentication | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) | 
| **POST** | /idTokenCheck/ | User token validation | [<img src="https://avatars.githubusercontent.com/u/49235528?s=70&v=4" width="30px">](https://github.com/oereo) | 
| **POST** | /api/insert-dummy-user | Create virtual user data for DEMO | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /api/user-search | Response user whose name is containing the keyword | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) | 
| **GET** | /api/user-by-kakaoid | Response user data identified by a unique KakaoID | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) | 
<br>

### ⭐️ Game and matching related
| Request-Method | Request-URI | About | Written-By |
|:---:|:---:|:---:|:---:|
| **POST** | /game/api/create-room | Create private game room | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/check-room-full | Check if the room is full | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/send-invite | Send a invitation for private race | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /game/api/invitation-by-id | Spread the invitation to invited users | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/invitation-read | Accept and enter the invited race | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/invitation-reject | Reject and ignore the invited race | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/room-status-by-url | Check the room status by room-url | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/room-enter | Enter the public room | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/new-record | Create time record when the race starts | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/update-record | Update record when the user passes finish line | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/create-room-public | Create public game room | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /game/api/public-room-list | Get a list of accesible room  | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/enter-wait-room | Enter the clicked matching room (public)  | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/quit-wait-room | Quit the clicked matching room (public)  | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /game/api/ent-arrangement | Re-arrangement of waiting room users position  | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/create-ranking | Update user's fastest record  | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /game/api/speedy-ranking/<int:map_id> | Get speedy ranking by the track campus | [<img src="https://avatars.githubusercontent.com/u/62995632?s=70&v=4" width="30px">](https://github.com/ohjeeyoung) |
| **GET** | /game/api/univ-ranking | Get university ranking | [<img src="https://avatars.githubusercontent.com/u/62995632?s=70&v=4" width="30px">](https://github.com/ohjeeyoung) |
| **GET** | /game/api/personal-ranking | Get personal ranking | [<img src="https://avatars.githubusercontent.com/u/62995632?s=70&v=4" width="30px">](https://github.com/ohjeeyoung) |
| **GET** | /game/api/sync-wait-room-status | Matching wait-room data sync | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **POST** | /game/api/room-to-start-status | Switch room status to start | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /game/api/room-status | Check the room status | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /game/api/game-enter | Moving users from the lobby to the game  | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /game/api/end-check | Check if any of the participants arrives at the end line  | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |
| **GET** | /game/api/result-board | Get the game result data (Ranking, Lap-time) | [<img src="https://avatars.githubusercontent.com/u/39653584?s=48&v=4" width="30px">](https://github.com/youngkwon02) |

---
<br>

# 🧑🏻‍💻 Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/youngkwon02"><img src="https://avatars.githubusercontent.com/u/39653584?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Youngkwon Kim</b></sub></a><br />Main Developer<br /><a href="https://github.com/Campus-Run/django-server/commits?author=youngkwon02" title="Documentation">⭐️</a></td>
        <td align="center"><a href="https://github.com/oereo"><img src="https://avatars.githubusercontent.com/u/49235528?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sehoon In</b></sub></a><br />Sub Developer<br /><a href="https://github.com/Campus-Run/django-server/commits?author=oereo" title="Documentation">⭐️</a></td>
        <td align="center"><a href="https://github.com/ohjeeyoung"><img src="https://avatars.githubusercontent.com/u/62995632?s=70&v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jeeyoung Oh</b></sub></a><br />Sub Developer<br /><a href="https://github.com/Campus-Run/django-server/commits?author=ohjeeyoung" title="Documentation">⭐️</a></td>
  </tr>
</table>
