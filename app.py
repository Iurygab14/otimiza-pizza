from flask import Flask, render_template, request
import pulp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    resultado = None

    if request.method == "POST":

        massa = float(request.form["massa"])
        queijo = float(request.form["queijo"])
        molho = float(request.form["molho"])
        calabresa_estoque = float(request.form["calabresa"])

        prob = pulp.LpProblem("Pizza", pulp.LpMaximize)

        x = pulp.LpVariable("Mucarela", lowBound=0, cat="Integer")
        y = pulp.LpVariable("Calabresa", lowBound=0, cat="Integer")

        prob += 20*x + 25*y

        prob += 0.5*x + 0.5*y <= massa
        prob += 0.3*x + 0.2*y <= queijo
        prob += 0.2*x + 0.2*y <= molho
        prob += 0.15*y <= calabresa_estoque

        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        resultado = {
            "mucarela": int(x.varValue),
            "calabresa": int(y.varValue),
            "lucro": int(pulp.value(prob.objective))
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)