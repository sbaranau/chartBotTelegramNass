import logging
import os
import openai
import data
import faiss
import numpy as np

file_path = "structured_document.txt"  # Specify your file path


class GPT:
    def __init__(self, openai_key):
        openai.api_key = openai_key
        os.environ["OPENAI_API_KEY"] = openai_key
        self.history_chat = []
        self.index = None
        self.texts = None

    @staticmethod
    def split_text_into_chunks(text: str, chunk_size: int, chunk_overlap: int):
        source_chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            source_chunks.append(chunk)
            start += chunk_size - chunk_overlap
        return source_chunks

    @staticmethod
    def search_faiss_index(query, index, texts, top_k=3):
        response = openai.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = np.array(response.data[0].embedding, dtype=np.float32)
        distances, indices = index.search(np.array([query_embedding]), top_k)
        return [texts[idx] for idx in indices[0] if idx < len(texts)]

    @staticmethod
    def generate_answer(system, instruction, summary_history, relevant_texts):
        message_content = '\n--------------------\n'.join(relevant_texts)
        user_content = f"{instruction}\n\nКонтекст:\n{message_content}\n\nИстория диалога:\n{summary_history}\n\nОтвет:"
        return GPT.generate_gpt_request(system, user_content)

    @staticmethod
    def generate_follow_up_question(system, instruction, summary_history, relevant_texts):
        message_content = '\n--------------------\n'.join(relevant_texts)
        user_content = f"{instruction}\n\nКонтекст:\n{message_content}\n\nИстория диалога:\n{summary_history}\n\nДополнительный вопрос:"
        return GPT.generate_gpt_request(system, user_content)

    @staticmethod
    def generate_gpt_request(system, user_content):
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content}
        ]
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        return completion.choices[0].message.content

    def init_bot(self, chunk_size=1024, chunk_overlap=100):
        logging.info("Разделение текста на чанки...")

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        self.texts = self.split_text_into_chunks(text, chunk_size, chunk_overlap)

        logging.debug("Создание FAISS индекса с OpenAI embeddings...")
        embeddings = []
        for chunk in self.texts:
            response = openai.embeddings.create(
                input=chunk,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding
            embeddings.append(embedding)

        embeddings = np.array(embeddings, dtype=np.float32)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        logging.debug(f"Индекс создан. Количество чанков: {len(self.texts)}")
        logging.debug(f"БОТ: {data.initial_question}")
        self.history_chat.append(f"БОТ: {data.initial_question}")

    def ask_chart_gpt(self, message):
        client_question = message.strip()
        if client_question.lower() in ['stop', 'стоп']:
            logging.debug("Завершаю диалог. Всего доброго!")
            return "Главное меню"

        self.history_chat.append(f"КЛИЕНТ: {client_question}")
        relevant_texts = self.search_faiss_index(client_question, self.index, self.texts)

        answer = self.generate_answer(
            system=data.system_prompt,
            instruction=data.instruction_prompt,
            summary_history='\n'.join(self.history_chat),
            relevant_texts=relevant_texts
        )
        logging.debug(f"БОТ: {answer}")
        self.history_chat.append(f"БОТ: {answer}")

        follow_up_question = self.generate_follow_up_question(
            system=data.system_prompt,
            instruction=data.follow_up_instruction,
            summary_history='\n'.join(self.history_chat),
            relevant_texts=relevant_texts
        )
        logging.debug(f"БОТ: {follow_up_question}")
        self.history_chat.append(f"БОТ: {follow_up_question}")

        return answer + "\n\n" + follow_up_question