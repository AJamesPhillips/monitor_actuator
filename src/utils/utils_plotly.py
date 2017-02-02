
def create_new_plot(plotly_username, plotly_api_key, plotly_streaming_token, filename, maxpoints=60*24):
    import plotly.plotly as plty

    plty.sign_in(plotly_username, plotly_api_key)

    url = plty.plot([
        {
            'x': [], 'y': [], 'type': 'scatter',
            'stream': {
                'token': plotly_streaming_token,
                'maxpoints': maxpoints
            }
        }], filename=filename)

    return url
