from instructor import MultiTask
import openai
from lib.types import CodeResult, SubTask

COMPONENTS = """
-Typography:Styles for headings, paragraphs, lists...etc
-Accordion:A vertically stacked set of interactive headings that each reveal a section of content.
-Alert:Displays a callout for user attention.
-Alert Dialog:A modal dialog that interrupts the user with important content and expects a response.
-Aspect Ratio:Displays content within a desired ratio.
-Avatar:An image element with a fallback for representing the user.
-Badge:Displays a badge or a component that looks like a badge.
-Button:Displays a button or a component that looks like a button.
-Calendar:A date field component that allows users to enter and edit date.
-Card:Displays a card with header, content, and footer.
-Checkbox:A control that allows the user to toggle between checked and not checked.
-Collapsible:An interactive component which expands/collapses a panel.
-Combobox:Autocomplete input and command palette with a list of suggestions.
-Command:Fast, composable, unstyled command menu for React.
-Context Menu:Displays a menu to the user — such as a set of actions or functions — triggered by a button.
-Data Table:Powerful table and datagrids built using TanStack Table.
-Date Picker:A date picker component with range and presets.
-Dialog:A window overlaid on either the primary window or another dialog window, rendering the content underneath inert.
-Dropdown Menu:Displays a menu to the user — such as a set of actions or functions — triggered by a button.
-React Hook Form:Building forms with React Hook Form and Zod.
-Hover Card:For sighted users to preview content available behind a link.
-Input:Displays a form input field or a component that looks like an input field.
-Label:Renders an accessible label associated with controls.
-Menubar:A visually persistent menu common in desktop applications that provides quick access to a consistent set of commands.
-Navigation Menu:A collection of links for navigating websites.
-Popover:Displays rich content in a portal, triggered by a button.
-Progress:Displays an indicator showing the completion progress of a task, typically displayed as a progress bar.
-Radio Group:A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time.
-Scroll-area:Augments native scroll functionality for custom, cross-browser styling.
-Select:Displays a list of options for the user to pick from—triggered by a button.
-Separator:Visually or semantically separates content.
-Sheet:Extends the Dialog component to display content that complements the main content of the screen.
-Skeleton:Use to show a placeholder while content is loading.
-Slider:An input where the user selects a value from within a given range.
-Switch:A control that allows the user to toggle between checked and not checked.
-Table:A responsive table component.
-Tabs:A set of layered sections of content—known as tab panels—that are displayed one at a time.
-Textarea:Displays a form textarea or a component that looks like a textarea.
-Toast:A succinct message that is displayed temporarily.
-Toggle:A two-state button that can be either on or off.
-Tooltip:A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it.
-Badge:Displays a badge or a component that looks like a badge.
-Calendar:A date field component that allows users to enter and edit date.
""".strip()

RULES = """
Here are some rules that you must follow when generating react code

1. Always add a title and description to a toast
```
onClick={() => {
  toast({
    title: <title goes here>,
    description: <description>,
  })
}}
```
2. Make sure to only use imports that follow the following pattern
- 'React'
- '@/components/ui/<componentName>'
- 'next/'

No other libraries are allowed to be used
"""

MultiTaskObjects = MultiTask(SubTask)

def generate_sub_tasks(query):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    temperature=0.3,
    stream=False,
    functions=[MultiTaskObjects.openai_schema],
    function_call={"name": MultiTaskObjects.openai_schema["name"]},
    messages=[
        {
          "role": "system",
          "content": f"You are a senior software engineer who is very familiar with NextJS and the @shadcn/ui libary. You are about to be given a task by a user to create a new NextJS component."
        },
        {
          "role":"assistant",
          "content": "Before you start on your task, let's think step by step to come up with some sub-tasks that must be completed to achieve the task you are about to be given."
        },
        {
          "role":"assistant",
          "content":f"Here are some of the components avaliable for use\n{COMPONENTS}"
        },
        {
            "role": "user",
            "content": f"{query}",
        },
    ],
    max_tokens=1000,
  )
  queries = MultiTaskObjects.from_response(completion)

  return [i.task for i in list(queries)[0][1]]

def generate_code(ctx_string,user_prompt):
  gen_code: CodeResult = openai.ChatCompletion.create(
    model="gpt-4",
    response_model=CodeResult,
    max_retries=2,
    messages=[
        {
          "role": "system",
          "content": f"You are a NextJS expert programmer. You are about to be given a task by a user to fulfil an objective using only components and methods found in the examples below."
        },
        {
            "role":"assistant",
            "content":f"Here are some relevant examples that you should refer to. Only use information from the example. Do not invent or make anything up.\n {ctx_string}"
        },
        {
          "role":"assistant",
          "content":f"Please adhere to the following rules when generating components\n {RULES}"
        },
        {
            "role": "user",
            "content": f"{user_prompt}",
        },
    ]
  )
  return gen_code.code

