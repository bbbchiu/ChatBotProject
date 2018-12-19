# ReadMd

## FSM pic
![](https://i.imgur.com/w7jEIrt.png)

## 有關Chat Bot
* 我的Chat Bot有以下幾個功能
    * 記帳
    * 顯示記帳紀錄
    * 計算花費比例
### 記帳
* 使用者可以輸入他們的花費(有三種花費分類:食物、日用品、其他)，花費會被記錄起來(程式結束，資料會清空)
### 顯示記帳紀錄
* 使用者可以看到目前所記錄過的花費
### 計算花費比例
* 使用者可以看到三種分類所花的錢對全部花費的錢的比例

## States
### User && Ready
* User為inital state，Ready為Chat Bot被啟動後的狀態
* 使用者輸入 **"Good Morning"** ， 使state的狀態由user -> ready，Chat bot開始啟用
* 使用者輸入 **"Bye"** ， 使state的狀態由ready -> user，Chat bot被關閉

### ready && add/list/counting
* add/list/counting 分別為三種功能的state
    * add -> 記帳
    * list -> 顯示記帳紀錄
    * counting -> 計算花費比例
* 使用者輸入 **"add new data/show list/counting the data"** ， 使state的狀態由ready -> add/list/counting，開始三種功能
* 使用者輸入 **"back to menu"** ， 使state的狀態由add/list/counting -> ready，重新選擇功能

### add && database && spend
* add 是一開始選擇新增記帳資料所進入的state，進入add之後會出現postback按鈕來讓使用者選擇花費分類(食物、日用品、其他)
* database 是紀錄其花費分類
* spend 是紀錄其花費金額，並將花費分類跟花費金額存起來
* 當state到spend，整個add new data的過程已結束，可以輸入**"back to menu"**回到ready state


