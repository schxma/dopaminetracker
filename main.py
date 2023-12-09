from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Variáveis para armazenar as dopaminas
dopaminas_positivas = {
    'Correr': 5,
    'Banho': 5,
    'Malhar': 3,
    'Se alongar': 1,
    'Meditar': 2,
    'Ler': 5
}
dopaminas_negativas = {
    'Usar rede social por 10 minutos': -20,
    'TikTok/Reels': -30,
    'Conteúdo adulto': -60,
    'Jogar video game por mais de 30 minutos': -20,
    'Drogas/Álcool': -50,
    'Comer doce': -10
}
recompensas = {}

# Total de pontos inicial
total_pontos = 100


@app.route('/')
def index():
    return render_template('index.html',
                           dopaminas_positivas=dopaminas_positivas,
                           dopaminas_negativas=dopaminas_negativas,
                           recompensas=recompensas,
                           total_pontos=total_pontos)


@app.route('/adicionar_atividade', methods=['POST'])
def adicionar_atividade():
    global total_pontos
    quantidade_positiva = sum(
        int(request.form.get(f'quantidade_positiva_{atividade}', 0) or 0) * dopaminas_positivas[atividade]
        for atividade in dopaminas_positivas
    )
    quantidade_negativa = sum(
        int(request.form.get(f'quantidade_negativa_{atividade}', 0) or 0) * dopaminas_negativas[atividade]
        for atividade in dopaminas_negativas
    )

    total_pontos += quantidade_positiva + quantidade_negativa
    if total_pontos < 0:
        total_pontos = 0  # Certificando-se de que a pontuação não seja negativa

    return redirect(url_for('index'))


@app.route('/adicionar_recompensa', methods=['POST'])
def adicionar_recompensa():
    global total_pontos
    recompensa = request.form['recompensa']
    custo = int(request.form['custo'])

    if total_pontos >= custo:
        recompensas[recompensa] = custo
        total_pontos -= custo

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
