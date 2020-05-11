import sys 
import requests    
base_url = "https://api.trello.com/1/{}" 
auth_params = {    
    'key': "2a6fe6ee63cd1456dedd20835930017f",    
    'token': "f0347c8b6a8e1709fb077c5ab5faed1380ccc4efe8337b357fabd8d3e9217942", }
board_id = "tIEcTi3J"    
    
def read():      
    
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        #print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print('{} (количество задач: {})'.format(column['name'], len(task_data)))      
        if not task_data:      
            net_zadach = '\t' + 'Нет задач!'     
            continue      
        for task in task_data:      
            print('\t' + task['name'])  
  
    
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            print('Задача создана')            
        break  
    
def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти все задачи по имени и получить их id    
    task_id = None
    find_tasks = [] #для списка найденных задач
    wrong_num=0 # для проверки, если задач с именем несколько, но при вводе введен неправильный номер
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                find_tasks.append(task_id)    
    #print (find_tasks)
    #print("Кол-во задач с таким именем", len(find_tasks))
    i = 0 #для номера задачи
    ii=[] # список для номеров найденных задач
    for card in find_tasks:
        i+=1
        ii.append(i)
        card_data = requests.get(base_url.format('cards') + '/' + card, params=auth_params).json()
        #для названия списка, с котором находится задача
        list_data_card = requests.get(base_url.format('list') + '/' + card_data['idList'], params=auth_params).json()
        #если задач с таким названием больше одной, выводим их список
        if len(find_tasks) > 1:
            print('{}. Задача "{}", описание задачи: "{}" в колонке "{}"'.format(i, card_data['name'], card_data['desc'], list_data_card['name']))
            
    #Если задач с таким названием больше одной, запрашиваем номер задачи, которую надо переместить   
    if len(find_tasks) > 1:
        x = input('Введите номер задачи, которую нужно переместить ')
        x = int(x)
        #print ("Номер задачи для перемещения",x)
            
        if x in ii:
            #print("номер задачи введен верно")
            #print(find_tasks[x-1])
            task_id = find_tasks[x-1]
        else:
            print("Номер задачи введен неверно")
            wrong_num=1
    elif len(find_tasks) == 0:
        print("Задачи с таким именем нет")
    else: 
        task_id = find_tasks[0]
        #print("одна задача", task_id)

       
    #print(task_id)   
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    flag = 0 #для проверки правильности ввода названия колонки
    #if task_id is not None:
    if len(find_tasks) != 0 and wrong_num==0:
        #print ("есть что перемещать")
        for column in column_data:    
            if column['name'] == column_name:   
                flag = 1;
                # И выполним запрос к API для перемещения задачи в нужную колонку    
                requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
                print("Задача перенесена")
                break
        if flag != 1:
            print ("Колонки с таким названием на доске нет")

def create_list(name):
    col_names=[]
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:
        col_names.append(column['name'])
        #print(column['name'])
    #print (col_names)
    if name in col_names:
        print('Колонка с таким именем уже есть')
    else:
        requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': name, **auth_params})
        print ("Колонка создана")
    
if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_list':    
        create_list(sys.argv[2])        
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])