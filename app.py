from flask import Flask, request, jsonify ,render_template
import pickle

app = Flask(__name__)


with open('content_based_data.pkl', 'rb') as f:
    content_data = pickle.load(f)

cosine_sim = content_data['cosine_sim']
indices = content_data['indices']
jobs = content_data['jobs']

def get_recommendations(title):
    try:
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        job_indices = [i[0] for i in sim_scores[1:11]]
        return jobs.iloc[job_indices][['Title', 'Description', 'City', 'State']].reset_index(drop=True)
    except KeyError:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
@app.route('/')
def home():
    return render_template('home.html')

    
    
@app.route('/get_jobs_content_based', methods=['POST'])
def get_jobs_content_based():
    try:
        job_title = request.form['job_title']
        job_recommendations = get_recommendations(job_title)
        
        if job_recommendations is not None:
            job_list = job_recommendations.to_dict(orient='records')
            return render_template('recommendations.html', recommendations=job_list) 
        else:
            return render_template('recommendations.html', recommendations=[]) 
    except Exception as e:
        return render_template('recommendations.html', recommendations=[]) 

if __name__ == '__main__':
    app.run(debug=True)
