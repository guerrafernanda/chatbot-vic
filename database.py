import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('acceptable_answers_db.sqlite')
        return conn
    except Error as e:
        print(e)

def create_table(conn):
    try:
        sql = ''' CREATE TABLE AcceptableAnswers (
                                    id integer PRIMARY KEY,
                                    question text NOT NULL,
                                    acceptable_answer text NOT NULL,
                                    rating text
                                ); '''
        cur = conn.cursor() 
        cur.execute(sql)
    except Error as e:
        print(e)

conn = create_connection()

if conn is not None:
    create_table(conn)
else:
    print("Error! Cannot create the database connection.")

def insert_answer(conn, answer):
    sql = ''' INSERT INTO AcceptableAnswers(question, acceptable_answer, rating)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, answer)
    conn.commit()
    return cur.lastrowid


data = [
    ("Using the tables {'sales': ['id', 'value', 'date_sales', 'quantity', 'product_id'], 'products': ['id', 'name']}, write a query to show the total number of sales in the last 6 months starting from 10/1/2023.", "SELECT COUNT(*) FROM sales WHERE date_sales BETWEEN '2023-10-01' AND DATE_ADD('2023-10-01', INTERVAL 6 MONTH); SELECT COUNT(*) FROM sales WHERE date_sales BETWEEN '2023-10-01' AND '2022-10-08';", "Excellent"),
    
    ("Write a query to show the top 5 best selling products since 10/1/2023.", "SELECT p.name, SUM(s.quantity) AS total_quantity FROM sales s JOIN products p ON s.product_id = p.id WHERE s.date_sales >= '2023-10-01' GROUP BY p.id, p.name ORDER BY total_quantity DESC LIMIT 5;", "Excellent"),
    
    ("A customer asks for a report of all sales over R$10 made between 10/01/2023 and 10/02/2023.", "SELECT * FROM sales WHERE value > $10 AND date_sales BETWEEN '2023-10-01' AND '2023-10-02'", "Excellent"),
    
    ("How do you imagine the day-to-day life of a Customer Support Engineer?", "Solving problems", "Excellent"),
    
    ("Why did you choose customer service?", "I enjoy solving problems, creating meaningful connections with customers and solving their needs, customer service allows me to develop communication, empathy and problem solving skills, which I consider essential for professional success", "Excellent"),
    
    ("What is your salary expectation?", "Up to 3.500 reais", "Excellent"),
    
    ("What is your salary expectation?", "More than 4.000 reais", "Not acceptable"),
    
    ("Describe a situation where you had to overcome a significant challenge at work. How did you do it and what did you learn from it?", "In a previous situation, we faced a challenge in launching a new product. An unexpected error occurred in the testing phase and, although it was somewhat complicated, I managed to notify a person on the team who managed to resolve the issue in a few hours", "Not acceptable"),
    
    ("Describe a situation where you had to overcome a significant challenge at work. How did you do it and what did you learn from it?", "In my last position, we were implementing a new customer support system. A few days before launch, we noticed that there was a critical error that prevented the system from working properly. Faced with this challenge, I decided to take the lead to solve the problem. I prioritized the tasks, coordinated with the team and was able to find the source of the error. Despite the stress and pressure, we worked together and were able to fix the issue in time for launch", "Excellent"),
    
    ("In your professional experience, what was the most challenging project or initiative you took on your own? How did you manage all the stages of this project and what did you do to ensure its success?", "On a previous project, I was assigned to lead a process improvement initiative. Throughout the project, I encountered significant challenges and obstacles. I raised my hand and communicated to my co-workers about the difficulties I was facing, but unfortunately the company did not provide me with the necessary support to overcome these obstacles. I ended up not being able to complete the project as planned", "Not acceptable"),
    
    ("In your professional experience, what was the most challenging project or initiative you took on your own? How did you manage all the stages of this project and what did you do to ensure its success?", "In my previous job, I noticed that the internal communication process in the company was quite fragmented and inefficient. I decided to take responsibility for this issue and proposed the creation of a new, more integrated and effective internal communication system. For this, I researched different tools available, held meetings with the teams involved, prepared an implementation plan and worked together with the IT team to put the new system into practice. In addition, I developed training for employees on the new platform. This initiative resulted in more fluid and collaborative communication between departments, improving the efficiency and productivity of the company as a whole", "Excellent"),
    
    ("Describe a situation where you came up with an innovative idea to improve a process, product or service in your previous job. How did you present this idea and what were the results achieved?", "Although I worked in an environment where innovation was valued, I didn't have the opportunity to bring an innovative idea to improve a specific process or service. While I've kept up to date on trends and news in the field, I haven't yet had a chance to apply these ideas in a meaningful way to my previous work. However, I look forward to having the opportunity to contribute innovative ideas in this position and to work in an environment that values ​​creativity and the pursuit of continuous improvement", "Not acceptable"),
    
    ("Describe a situation where you came up with an innovative idea to improve a process, product or service in your previous job. How did you present this idea and what were the results achieved?", "In my previous job, I realized that there was an opportunity to improve the efficiency of the customer service process. I proposed implementing a chatbot system to handle the most common queries from customers. To present this idea, I prepared a feasibility study, highlighting the benefits and savings in time and resources that we could achieve. I presented the proposal at a team meeting and received support to move forward. After implementing the chatbot, we noticed a significant reduction in response time to customers, as well as an overall improvement in the customer experience. This innovative idea not only streamlined our internal processes, but also brought tangible benefits to our customers", "Excellent"),
    
    ("Describe a situation in which you showed enthusiasm and interest in learning and applying knowledge in technologies such as SQL, Python, ChatGPT or any other that you consider relevant in your previous work. How did you keep up to date with these technologies and how did you use them to improve your professional activities?", "I used ChatGPT to ask basic questions or search for simple information, but I didn't explore the full potential of this technology. Also, I've studied SQL for the current position, but I haven't had the opportunity to practically apply it in a real project. Although I have theoretical knowledge in these technologies, I still haven't been able to use them in real situations. However, I am willing to expand my experience and apply this knowledge to future projects", "Not acceptable"),
    
    ("Describe a situation in which you showed enthusiasm and interest in learning and applying knowledge in technologies such as SQL, Python, ChatGPT or any other that you consider relevant in your previous work. How did you keep up to date with these technologies and how did you use them to improve your professional activities?", "In my previous job, I was enthusiastic about learning and applying new technologies like Python. I stayed current through online courses, books, and participation in developer communities. A specific example of how I applied this technology was when I developed an automated Python script for real-time data analysis. This script was capable of extracting raw data, processing it and generating ready-to-use reports. This automation allowed the team to save hours of manual work and make faster and more accurate decisions. In addition, I also explored other technologies such as SQL to optimize queries and improve database performance. These innovative technology application initiatives brought significant improvements to work and were recognized by the team and managers", "Excellent"),
    
    ("Why are you interested in working at CloudWalk as a Customer Support Engineer? What specifically appeals to you about the company's culture, products/services, or mission? How do you see yourself contributing to the company's long-term success?", "I chose CloudWalk as a job option because it offers an attractive salary and interesting benefits, such as a home office. I believe I can gain experience here before looking for better opportunities in the future; I am interested in the job at CloudWalk because I believe I can achieve a good work-life balance. Also, I heard that the company has a good reputation in the market, which could open doors to other career opportunities; The main reason I am interested in working at CloudWalk is because I see the company growing rapidly and there are opportunities for career advancement. I want to take advantage of these opportunities to advance my career path, even if I'm not particularly passionate about the company's products or services", "Not acceptable"),
    
    ("Why are you interested in working at CloudWalk as a Customer Support Engineer? What specifically appeals to you about the company's culture, products/services, or mission? How do you see yourself contributing to the company's long-term success?", "I am very interested in working at CloudWalk as a Customer Support Engineer, as I deeply admire the culture of innovation and excellence that the company promotes. Furthermore, I am passionate about the products and services offered by CloudWalk, which are revolutionizing the payment industry. I see myself contributing to the company's long-term success by providing exceptional support to customers, efficiently resolving their issues and helping to create a world-class user experience. I'm excited to be part of a talented and collaborative team that shares the same values ​​and is committed to taking the company to the next level; CloudWalk is a company that values ​​continuous learning and development for its employees, which is something I really admire. I am excited about the opportunity to work in a dynamic environment where I can improve my technical skills and learn from talented professionals. Additionally, CloudWalk's mission to democratize access to innovative and secure payment solutions resonates deeply with my values. I want to be a part of this transformation journey, supporting customers and helping drive the company's growth and success; I chose CloudWalk as my dream company to work as a Customer Support Engineer because I am passionate about technology and innovation. The company's culture, based on teamwork, respect and employee empowerment, is something that deeply appeals to me. I believe that by working in an environment where my ideas are valued and encouraged, I can make a significant contribution to the improvement of CloudWalk's products and services. I am motivated to tackle complex customer support challenges, providing effective solutions and ensuring customer satisfaction. My goal is to grow together with the company, facing new challenges and helping drive CloudWalk's innovation and success", "Excellent"),
    
    ("Why are you interested in working at CloudWalk as a Customer Support Engineer? What specifically appeals to you about the company's culture, products/services, or mission? How do you see yourself contributing to the company's long-term success?", "I don't know", "Not acceptable"),
    
    ("Describe a situation in which you showed enthusiasm and interest in learning and applying knowledge in technologies such as SQL, Python, ChatGPT or any other that you consider relevant in your previous work. How did you keep up to date with these technologies and how did you use them to improve your professional activities?", "I don't know", "Not acceptable"),
    
    ("Describe a situation where you came up with an innovative idea to improve a process, product or service in your previous job. How did you present this idea and what were the results achieved?", "I don't know", "Not acceptable"),
    
    ("In your professional experience, what was the most challenging project or initiative you took on your own? How did you manage all the stages of this project and what did you do to ensure its success?", "I don't know", "Not acceptable"),
    
    ("Describe a situation where you had to overcome a significant challenge at work. How did you do it and what did you learn from it?", "I don't know", "Not acceptable"),
    
    ("A entrega da maquininha está atrasada! O que vão fazer a respeito?", "Primeiramente sinto muito pela experiência ruim que teve conosco. Não é esse tipo de situação que queremos proporcionar para nossos clientes. Acabei de abrir um chamado na transportadora para realizarem a investigação do que pode ter ocorrido,  além de solicitar urgência na entrega da sua máquina. Fique tranquilo que vou cuidar do seu caso pessoalmente, consultarei o status da entrega até que de fato seja realizada. Não consigo te afirmar que a entrega será amanhã, mas pode ter certeza que o seu caso já está sendo visto com prioridade. Mais uma vez peço desculpas por isso e sigo à disposição para te ajudar", "Excellent"),
    
    ("A entrega da maquininha está atrasada! O que vão fazer a respeito?", "Já foi aberto um chamado para resolver. Qualquer dúvida entre em contato conosco", "Not acceptable"),
    
    ("Minha maquininha não segura a bateria/carga e agora me disseram que ela está fora da garantia e não podem trocar. Tem como não ter custos?", "Primeiramente sentimos muito pela experiência ruim que teve conosco. Não é esse tipo de situação que queremos proporcionar para nossos clientes. Eu entendo de verdade que,  precisar da máquina e ela não conseguir aguentar a bateria pode prejudicar o seu negócio. Vou resolver o seu problema, Paula, mas antes preciso lembrar que, assim como qualquer outro aparelho (por ex. celular) existe o tempo de garantia e, se o contato for após este prazo, infelizmente perde a cobertura. Nós temos este custo pelos processos operacionais nesta situação de troca,  mas devido ao seu tempo conosco e por utilizar nosso produto recorrentemente, eu verifiquei com a área responsável e consigo aplicar um desconto de 40% no valor total do custo", "Excellent"),
    
    ("Minha maquininha não segura a bateria/carga e agora me disseram que ela está fora da garantia e não podem trocar. Tem como não ter custos?", "Não tem como fazer nada, a garantia já expirou e você precisará arcar com os custos. Qualquer outra dúvida entre em contato conosco", "Not acceptable"),
    
    ("Eu não recebi um valor que era para ter caído ontem, o que houve? Tenho contas para pagar!", "Primeiramente sentimos muito pela experiência ruim que teve conosco. Não é esse tipo de situação que queremos proporcionar para nossos clientes. Infelizmente ontem nós passamos por instabilidades e nos comprometemos a sempre sermos transparentes com você e trabalhar para resolver o problema com a maior brevidade possíve. Já reenviamos os valores de recebíveis para pagamento hoje. Pedimos por gentileza que aguarde até o final do dia, lembrando que os depósitos podem ocorrer de maneira fracionada. Sigo à disposição aqui no chat para qualquer outra dúvida que você tiver", "Excellent"),
    
    ("Eu não recebi um valor que era para ter caído ontem, o que houve? Tenho contas para pagar!", "Os pagamentos foram enviados novamente. Qualquer dúvida entre em contato conosco", "Not acceptable")
]

for answer in data:
    insert_answer(conn, answer)


