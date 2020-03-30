import os
import config
import requests
# from flask import request
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

external_stylesheets = [
    "https://use.fontawesome.com/releases/v5.0.7/css/all.css",
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    'https://fonts.googleapis.com/css?family=Roboto&display=swap'
]

app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True
)

app.title = 'Amazon Reviews'

app.layout = html.Div(
    [
        html.H1(
            [
                "What do you think of this product?"
            ],
            className="h3 mb-3 font-weight-normal",
            style={
                'marginTop': '5px'
            }
        ),

        html.Div(
            [
                dcc.Textarea(
                    className="form-control z-depth-1",
                    id="review",
                    rows="8",
                    placeholder="Write something here..."
                )
            ],
            className="form-group shadow-textarea"
        ),

        html.H5(
            'Sentiment Analysis 🤖'
        ),

        dbc.Progress(
            children=html.Span(
                id='proba',
                style={
                    'color': 'black',
                    'fontWeight': 'bold'
                }
            ),
            id="progress",
            striped=False,
            animated=False,
            style={
                'marginBottom': '10px'
            }
        ),

        html.H5(
            'Propose a rating 📢'
        ),

        html.Div(
            [
                dcc.Slider(
                    id='rating',
                    max=5,
                    min=1,
                    step=1,
                    marks={i: f'{i}' for i in range(1, 6)}
                ),
            ],
            style={'marginBottom': '30px'}
        ),

        html.Button(
            [
                html.Span(
                    "Submit",
                    style={
                        "marginRight": "10px"
                    }
                ),
                html.I(
                    className="fa fa-paper-plane m-l-7"
                )
            ],
            className="btn btn-lg btn-primary btn-block",
            role="submit",
            id="submit_button",
            n_clicks=0
        )
    ],
    className="form-review",
)


@app.callback(
    [
        Output('review', 'value')
    ],
    [
        Input('submit_button','n_clicks')
    ],
    [
        State('review', 'value'),
        State('rating','value')
    ]
)

def submit_review(n_clicks, review_text, review_label):
    ''' Submit review and update text box '''

    if n_clicks:
        response = requests.post(f'{config.API_URL}/review',
        data = {'review_label': review_label, 'text': review_text})

        if response.ok:
            print('Review Saved')
        else:
            print('Error Saving Review')

    return ('',)
        

@app.callback(
    [
        Output('proba', 'children'),
        Output('progress', 'value'),
        Output('progress', 'color'),
        Output('rating', 'value'),
        Output('submit_button', 'disabled')
    ],
    [Input('review', 'value')]
)

def update_proba(review):
    ''' Request model prediction from API and update progress bar and suggested rating '''

    # Make sure empty reviews don't get scored
    if review is not None and review.strip() != '':
        # POST request to acquire prediction score from model
        response = requests.post(f'{config.API_URL}/predict', data={'text': review})
        proba_positive = response.json()
        proba_positive = round(proba_positive*100, 2)
        suggested_rating = min(int(proba_positive/100 * 5 + 1), 5)
        text_proba = f"{proba_positive}%"

        if proba_positive >= 67:
            return text_proba, proba_positive, 'success', suggested_rating, False
        elif 33 < proba_positive < 67:
            return text_proba, proba_positive, 'warning', suggested_rating, False
        elif proba_positive <= 33:
            return text_proba, proba_positive, 'danger', suggested_rating, False
    else:
        return None, 0, None, 0, True

if __name__ == '__main__':
    app.run_server(debug = config.DEBUG, host = config.HOST)
