from flask import Blueprint, render_template, redirect, url_for, request
from application.text_checker.text_matcher import find_matches_with_score_higher_than, find_random_matches
import re
from application.search.search_form import SearchQueryForm

search_bp = Blueprint("search_bp", __name__, template_folder="templates", static_folder="static")
score_threshold = 65

@search_bp.route('/')
def search_home():
  form = SearchQueryForm(request.args, meta={'csrf': False})
  return render_template('home.html', form=form)

@search_bp.route('/search', methods=('GET', 'POST'))
def search_results():
  matches = []

  form = SearchQueryForm(request.args, meta={'csrf': False})
  if form.validate():
    matches = find_matches_with_score_higher_than(score_threshold, form.data['query'])

    if "COVID-19" in form.data['query'] and "corona virus" not in form.data['query']:
      # Rerun with corona virus
      query = form.data['query'].replace("COVID-19", "corona virus")
      matches += find_matches_with_score_higher_than(score_threshold, query)
    elif "corona virus" in form.data['query'] and "COVID-19" not in form.data['query']:
      query = form.data['query'].replace("corona virus", "COVID-19")
      matches += find_matches_with_score_higher_than(score_threshold, query)

    matches.sort(key=lambda x: x['score'], reverse=True)
    matches = matches[0:15]
  else:
    return redirect(url_for('search_bp.search_home'))
  # add source url
  pnt_url = "https://www.poynter.org/?ifcn_misinformation="
  for idx in range(len(matches)):
    title = matches[idx]['title']
    matches[idx]['url'] = pnt_url + re.sub('[^A-Za-z0-9 -]+', '', title).replace(' ', '-')

  return render_template('results.html', matches = matches, form=form)
