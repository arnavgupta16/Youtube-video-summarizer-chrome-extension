from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    summary = get_summary(get_transcript(video_id))
    return summary, 200

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    summarizer = pipeline('summarization')
    summary = ''
    word_count = 0

    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summarizer(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        sentences = summary_text.split('.')
        
        for sentence in sentences:
            words_in_sentence = sentence.split()
            if word_count + len(words_in_sentence) <= 200:
                summary += sentence + '. '
                word_count += len(words_in_sentence)
            else:
                break

    return summary

    

if __name__ == '__main__':
    app.run()