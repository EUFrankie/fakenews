from flask import Blueprint, render_template

home_bp = Blueprint("home_bp", __name__, template_folder="templates", static_folder="static")


@home_bp.route("/")
@home_bp.route("/home")
def home():
    team = ["dani", "elsa", "esther", "jan", "maurits", "myriam", "soutrik"]
    sources = {}
    information = {
        "dani": {
            "text": """“Data scientist with a master in Data Science and Entrepreneurship working as a freelance data scientist. 
                        Believes that data-driven solutions should improve people’s life. Frankie is a tool to fight disinformation 
                        and protect society against its effects.” """,
            "linkedin": "https://www.linkedin.com/in/daniellepaesbarretto/",
            "twitter": "https://twitter.com/@DPaesBarretto"
        },
        "myriam": {
          "text": """“Mathematician working as a Data Analyst. I believe that technology should be used to empower 
          humans, not to cut their freedom. Frankie is the technological tool needed between quality journalism 
          and people.”""",
            "linkedin": "https://www.linkedin.com/in/myriambarnes/",
            "twitter": "https://twitter.com/myrbarnes_"
        },
        "esther": {
           "text": """“Civil rights' advocate and recovering development and humanitarian worker. Worries about media 
                        freedom and pluralism degrading in the EU. Trusts Frankie will
                        make citizens’ aware of the critical importance of investing in high-quality journalism.”""",
            "linkedin": "https://www.linkedin.com/in/esther-mart%C3%ADnez-gonz%C3%A1lez-15889512/",
            "twitter": "https://twitter.com/reclaim_esther"
        },
        "maurits": {
            "text": """“Data scientist and developer with a master in Business Engineering studying a data science 
            master to prepare for the future. A python enthusiast and believes in a world filled by trust. Frankie could
             play an important role to achieve this. “
            """,
            "linkedin": "https://www.linkedin.com/in/maurits-de-roover-338a6229",
            "twitter": ""
        },
        "jan": {

        }

    }

    for item in team:
        sources.update({item.capitalize(): 'team/pictures/{0}.png'.format(item)})
    return render_template("landingpage.html", team=sources)


@home_bp.route("/testing")
def testing():
    return render_template("testhome.html")


@home_bp.route("/test")
def test():
    return render_template("landingpage_testing.html")


@home_bp.route("/testmau")
def testmau():
    return render_template("landingpage_testmau.html")


@home_bp.route("/api_documentation")
def api_doc():
    return render_template("api_doc.html")


@home_bp.route("/team")
def team():
    return render_template("team.html")