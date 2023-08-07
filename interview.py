import pandas as pd
import openai
import datetime
import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())
openai.api_key = os.environ.get('OPENAI_API_KEY')

def load_questions(filename, tables):
    df = pd.read_csv(filename)
    questions = df['question'].tolist()
    questions = [q.format(tables=tables) for q in questions]
    return questions

tables = {
    'sales': ['id', 'number_sales', 'date_sales', 'quantity', 'product_id'],
    'products': ['id', 'name']
}

questions = load_questions('questions.csv', tables)

class Asker:
    def __init__(self, tables, questions):
        self.tables = tables
        self.questions = questions
        self.user_responses = []
        self.roleplay_questions = []
        self.roleplay_answers = []

    def chatbot(self):
        print(f"I will be asking you some questions, ok? Let's start our interview! You can type 'stop' to end the interview.")
        while True:
          print("Please type 'Ready' so we can start.")
          start_input = input()
          if start_input.lower() == 'ready':
              for i, question in enumerate(self.questions, start=1):
                    print(f"\nQuestion {i}:")
                    print(question)
                    response = input()
                    if response.lower() == 'stop':
                      print("Interview ended.")
                      return
                    self.user_responses.append(response)
                    model_response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an AI recruitment assistant responsible for conducting interviews with the candidates. You are very nice and enthusiastic."},
                            {"role": "user", "content": response},
                            {"role": "assistant", "content": "Your job is to thank the candidate for their answer. Just say a brief thank you, don't ask questions"},
                        ],
                        temperature=0.7,
                    )
                    model_message = model_response.choices[0].message['content']
                    print(model_message)
              break

    def roleplay(self):
        print("Vamos passar para a fase de encenação onde nosso assistente será um cliente fazendo algumas perguntas e você será o analista, ok? Agora você pode responder em Português. Escreva 'vamos lá' quando estiver pronto para começar nossa encenação!")
        while True:
          start_input = input()
          if start_input.lower() == 'vamos lá':
            break

        aspects = ["delivery of the machine is delayed", "the battery of the machine is not lasting as long and now it's not under warranty", "payments were not paid on time"]
        for i, aspect in enumerate(aspects):
            question_generation = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are conducting a roleplay for an interview in which you are an impolite customer asking questions on a chat, don't apologize. I want you to ask the user a question about {aspect}. Asks the questions in Portuguese. Example conversation: Cliente: A entrega da minha maquininha está atrasada! O que vão fazer? Analista: Primeiramente sinto muito pela experiência ruim que teve conosco. Não é esse tipo de situação que queremos proporcionar para nossos clientes. Acabei de abrir um chamado na transportadora para realizarem a investigação do que pode ter ocorrido,  além de solicitar urgência na entrega da sua máquina. Fique tranquilo que vou cuidar do seu caso pessoalmente, consultarei o status da entrega até que de fato seja realizada. Não consigo te afirmar que a entrega será amanhã, mas pode ter certeza que o seu caso já está sendo visto com prioridade. Mais uma vez peço desculpas por isso e sigo à disposição para te ajudar."}
                ],
                temperature=0.4,
            )

            question = question_generation["choices"][0]["message"]["content"]
            self.roleplay_questions.append(question)
            print(f"\n{question}")
            user_answer = input("Analista: ")
            if user_answer.lower() == 'stop':
                print("Interview ended.")
                return
            self.roleplay_answers.append(user_answer)

    def save_responses(self, filename_prefix):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'candidate_answers_{timestamp}.csv'
        df = pd.DataFrame({
        'question': self.questions + self.roleplay_questions,
        'answer': self.user_responses + self.roleplay_answers
        })
        df.to_csv(filename, index=False)

def interview_process(start_input):
    if start_input.lower() == 'ready':
        candidate_name = input("My name is Ronaldo! What's your name? ")
        print(f"Hello, {candidate_name}!")
        asker = Asker(tables)
        asker.chatbot()
        asker.roleplay()
        asker.save_responses()
        return "Obrigado por suas respostas! Com isso a entrevista está concluída!!"
    else:
        return "Please type 'Ready' when you are prepared to start."