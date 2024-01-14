from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.environ.get('OPEN_AI_API_KEY')

def get_product_name(title: str, openai_api_key) -> str:
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=openai_api_key, max_tokens=100)
    template = """
    I want you to get the product name from the title.
    title: {title} 
    Your answer should contain only a product name.
    """
    prompt_template = PromptTemplate(input_variables=["title"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    product_name = (chain.invoke(input={'title':title})['text'])
    assert type(product_name) == str
    return product_name

# if __name__ == '__main__':
#     product = get_product_name('앱코 H140r 4k 무선마우스 팝니다',openai_api_key)
#     print(product)