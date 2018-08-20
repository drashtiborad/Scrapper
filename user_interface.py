from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

from form import Search

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
es = Elasticsearch()


@app.route("/", methods=['GET', 'POST'])
def jobs():
    search_result = []
    from_page = -1
    data = Search()
    if request.method == 'GET':
        try:
            search_result = es.search(index='jobs', doc_type='job_description',
                                      body={'query': {'multi_match': {'query': request.args.get("search_text"),
                                                                      'type': 'most_fields',
                                                                      'fields': ['job_title^10', 'job_description',
                                                                                 'company',
                                                                                 'compensation', 'location'],
                                                                      'fuzziness': 'AUTO'}},
                                            'from': request.args.get("from_page", 0), 'size': 5})
            search_result = search_result["hits"]["hits"]
        except:
            pass
        from_page = int(request.args.get("from_page", -1))
        if len(search_result):
            from_page = int(request.args.get("from_page", 0))
    return render_template('search_engine.html', search_result=search_result, form=data, from_page=from_page,
                           search_text=request.args.get("search_text"))


if __name__ == '__main__':
    app.run(threaded=True)
