import json
from pydantic import Field,BaseModel
from typing import List
import instructor
from enum import Enum

instructor.patch()


class SubTask(BaseModel):
  """
  This is a class representing a sub task that must be completed in order for the user's request to be fulfilled.

  Eg. I want to have a login form that users can use to login with their email and password. If it's a succesful login, then we should display a small toast stating Congratulations! You've succesfully logged in.

  We can decompose our tasks into sub tasks such as
  - Create a input form that takes in an email
  - Create a primary button that has an onclick event
  - display a toast using the useToast hook

  and so on.
  """
  task:str = Field(description="This is an instance of a sub-task which is relevant to the user's designated task")

class CodeResult(BaseModel):
  """
  This is a class representing the generated code from a user's query. This should only include valid React Code that uses the @shadcn/ui library. Please make to conform to the examples shown
  """
  code:str

class Task(BaseModel):
  """
  This is a class which represents a potential task that could have resulted in the code snippet provided 

  eg. I want a button that generates a toast when it's clicked
  eg. I want a login form which allows users to key in their email and validates that it belongs to the facebook.com domain.
  """
  task: str = Field(description="This is a task which might have resultde in the component")

MultiTaskType = instructor.MultiTask(Task)

class TaskToCode(BaseModel):
   chunk:str
   taskList:List[str]
   componentName:str

class Query(BaseModel):
  """
  This is a sentence which will represent a potential user query or objective that the provided example will match.

  Eg. I want to create a button that will be able to generate a toast on a succesful request
  Eg. I want to create an component that has a large title and a subtitle which has a single element in bold
  """
  query_description:str = Field(description = "This is a meta-description of the query. Make sure to give at most 2 sentences of context about this potential query")
  user_query:List[str] = Field(description = "This is the user query that the provided example will match")
  keywords:List[str] = Field(description = "These are some keywords that are relevant to the generated user query")

class QueryWithCode(Query):
    chunk: str