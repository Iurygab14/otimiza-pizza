from flask import Flask, render_template
import pulp

app = Flask(__name__)

@app.route("/")
def home():

    prob = pulp.LpProblem("Pizza", pulp.LpMaximize)

    x = pulp.LpVariable("Mucarela", lowBound=0, cat="Integer")
    y = pulp.LpVariable("Calabresa", lowBound=0, cat="Integer")

    prob += 20*x + 25*y

    prob += 0.5*x + 0.5*y <= 10
    prob += 0.3*x + 0.2*y <= 5
    prob += 0.2*x + 0.2*y <= 4
    prob += 0.15*y <= 2

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    resultado = {
        "mucarela": int(x.varValue),
        "calabresa": int(y.varValue),
        "lucro": int(pulp.value(prob.objective))
    }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)