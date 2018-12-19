from transitions.extensions import GraphMachine

from utils import send_text_message,send_add_button_message


class TocMachine(GraphMachine):
    addCate = "None"

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_ready(self, event):
        f = open('./database.txt','w')
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'good morning'
        return False

    def is_going_to_add(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'add new data'
        return False

    def is_going_to_counting(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text.lower() == 'count the data':
                f = open("./database.txt","r")
                line = f.read()
                status = "none"
                f = 0.0
                d = 0.0
                o = 0.0
                num = 0.0
                piece = line.split()
                for x in piece:
                    if(status == "none"):
                        status = x
                    else:
                        if(status == "Food"):
                            f = f+float(x)
                        elif(status == "Daily_Necessity"):
                            d = d+float(x)
                        elif(status == "Others"):
                            o =o+float(x)
                        else:
                            pass
                        num = num+float(x)
                        status = "none"
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id,"Food")
                responese = send_text_message(sender_id,str(f/num))
                responese = send_text_message(sender_id,"Daily_necessity")
                responese = send_text_message(sender_id,str(d/num))
                responese = send_text_message(sender_id,"Others")
                responese = send_text_message(sender_id,str(o/num))
                return True
            else:
                return False
        return False

    def is_going_to_db(self,event):
        if event.get("postback"):
            text = event['postback']['title']
            if text == "Food":
                self.addCate = text
                print(text)
                return True
            elif text == "Daily_Necessity":
                self.addCate = text
                print(text)
                return True
            elif text == "Others":
                self.addCate = text
                print(text)
                return True
            else:
                return False
        return False

    def is_going_to_spend(self,event):
        f = open("./database.txt","a")
        if event.get("message"):
            text = event['message']['text']
            print(self.addCate)
            for c in text:
                if(c == '0' or c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' or c == '7' or c == '8' or c == '9'):
                    pass
                else:
                    break
            if(c == '0' or c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' or c == '7' or c == '8' or c == '9'):
                f.write(self.addCate)
                f.write(" ")
                f.write(text)
                f.write("\n")
                return True
            else:
                return False
        else:
            return False

    def is_going_to_list(self,event):
        if event.get("message"):
            text = event['message']['text']
            if text.lower() == 'show list':
                f = open("./database.txt","r")
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, f.read())
                return True
            else:
                return False
        else:
            return False

    def is_back_to_user(self,event):
        if event.get("message"):
            text = event['message']['text']
            if text.lower() == 'bye':
                sender_id = event['sender']['id']
                responese = send_text_message(sender_id, "Bye Bye~")
                return True
        return False

    def is_back_to_ready(self,event):
        if event.get("message"):
            text = event['message']['text']
            if text.lower() == 'back to menu':
                return True
        return False

    def on_enter_ready(self, event):
        print("I'm entering state1")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Good Morning~")

    def on_exit_ready(self,event):
        print('Leaving ready')

    def on_enter_add(self, event):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "Adding")
        send_add_button_message(sender_id)

    def on_exit_add(self,event):
        print('Leaving add')

    def on_enter_list(self, event):
        pass

    def on_exit_list(self,event):
        print('Leaving list')

    def on_enter_counting(self, event):
        pass

    def on_exit_counting(self,event):
        print('Leaving counting')

    def on_enter_database(self, event):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "How much did you spend?")

    def on_exit_database(self,event):
        print('Leaving db')

    def on_enter_spend(self, event):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "create data sucessfully")


    def on_exit_spend(self,event):
        print('Leaving state')
