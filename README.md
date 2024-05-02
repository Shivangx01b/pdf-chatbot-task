# pdf-chatbot-task
pdf-chatbot-task


## How to Run


a) Docker build
- Step 1
  ```docker build -t pdf_rag . ```

- Step 2
  ```docker run -it -e OPENAI_API_KEY="<your openai key>" -p 8000:8000 pdf_rag```

b) Send request

- Step 1
  First upload the pdf once api is up and running
  ```
  curl --location 'http://localhost:8000/upload' \
  --form 'file=@"/C:/Users/shivang/Downloads/handbook.pdf"'
  ```

- Step 2
  Ask your questions with the taskid received from "Step 1"
  ```
  curl --location 'http://localhost:8000/query' \
  --header 'Content-Type: application/json' \
  --data '{"taskid": "2580a111-8437-4e65-b483-0769e50b3a1f", "question": "What is shivang in Zania Inc"}'
  ```
  

