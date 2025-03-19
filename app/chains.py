import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("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"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        ch_extract = prompt_extract | self.llm
        result = ch_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            result = json_parser.parse(result.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return result if isinstance(result, list) else [result]

    def write_mail(self, job, links):
        email_draft = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Krutik Shah
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Krutik
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase: {link_list}
            Remember you are Krutik
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        email = email_draft | self.llm
        result = email.invoke({"job_description": str(job), "link_list": links})
        return result.content

if __name__ == "__main__":
    print(os.getenv("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"))