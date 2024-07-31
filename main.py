from fasthtml import FastHTML, picolink
from fasthtml.common import *
import random, uvicorn

charset = Meta('charset="utf-8"')
meta = Meta('name="viewport" content="width=device-width, initial-scale=1.0"')
css=Style("""
        .card {
            width: 100px;
            height: 150px;
            background-color: white;
            border: 1px solid black;
            border-radius: 10px;
            display: inline-flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 10px;
            margin: 10px;
            font-family: Arial, sans-serif;
            box-sizing: content-box;
        }

        .red {
            color: red;
        }

        .black {
            color: black;
        }

        .top-left, .bottom-right {
            font-size: 24px;
            font-weight: bold;
        }

        .bottom-right {
            align-self: flex-end;
            transform: rotate(180deg);
        }

        .suit {
            font-size: 48px;
            align-self: center;
        }
""")

suits = {"H":"♥", "S":"♠", "C":"♣", "D":"♦"}
colors = {"H":"red", "S":"black", "C":"black", "D":"red"}
values="23456789TJQKA"

def card(mycard):
    val = mycard[:-1]
    suit = suits[mycard[-1]]
    return Div(
        Div(val, cls="top-left"),
        Div(suit, cls="suit"),
        Div(val, cls="bottom-right"),
        cls="card "+colors[mycard[-1]])

app = FastHTML(hdrs=(picolink,css))
# app = FastHTML(hdrs=(css))


# @app.get("/")
# def home():
#     return Title("Test"),card("2H")

@app.get("/")
def home():
    initial_cards = [card(random.choice(values)+
                         random.choice("".join(suits.keys()))) for i in range(20)]
    return Title("Infinite Scroll Demo"), Main(
    H1("Infinite Scroll Demo"),
    Div(*initial_cards, id="card-container"),
    Div(
        hx_get="/more-cards",
        hx_trigger="intersect once",
        hx_swap="afterend",
        hx_target="#card-container"
    ),
    style="max-width: 800px; margin: 0 auto;"
)

@app.get("/more-cards")
def more_cards(request):
    # Get the current count from the query parameters
    start = int(request.query_params.get("start", 21))
    end = start + 20
    
    new_cards = [card(random.choice(values)+
                         random.choice("".join(suits.keys()))) for i in range(start, end)]
    
    return *new_cards, Div(
            hx_get=f"/more-cards?start={end}",
            hx_trigger="intersect once",
            hx_swap="afterend",
            hx_target="this"
        )

if __name__ == '__main__': uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)
# if __name__ == '__main__': uvicorn.run("main:app", reload=True)