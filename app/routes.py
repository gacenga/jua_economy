from flask import render_template, url_for, flash, redirect, jsonify
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from .models import User
from . import db
from flask_login import login_user, current_user, logout_user, login_required
from app.api.economic_data import EconomicDataFetcher
import requests

def init_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    flash('Incorrect password. Please try again.', 'danger')
            else:
                flash('Email not found. Please check your email or sign up.', 'danger')
        return render_template('home.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        return render_template('signup.html', title='Register', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/get-user-info', methods=['GET'])
    @login_required
    def get_user_info():
        user_info = {
            'name': current_user.username,
            'email': current_user.email
            }
        return jsonify(user_info)

    @app.route('/manage_account', methods=['GET', 'POST'])
    @login_required
    def manage_account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
            try:
                current_user.username = form.username.data
                current_user.email = form.email.data
                if form.password.data:
                    current_user.set_password(form.password.data)
                db.session.commit()
                flash('Your account has been updated successfully!', 'success')
                return redirect(url_for('manage_account'))
            except Exception as e:
                db.session.rollback()
                flash('There was an issue updating your account. Please try again.', 'danger')

        form.username.data = current_user.username
        form.email.data = current_user.email
        return render_template('manage_account.html', form=form)

    @app.route('/gdp')
    def gdp():
        fetcher = EconomicDataFetcher()
        try:
            gdp_data = fetcher.fetch_gdp_data()
            years = [entry['year'] for entry in gdp_data]
            gdp_values = [entry['gdp'] for entry in gdp_data]
            return render_template('gdp.html', labels=years, data=gdp_values)
        except requests.RequestException as e:
            flash(f"Error fetching GDP data: {e}", 'danger')
            return render_template('gdp.html', labels=[], data=[])

    @app.route('/trade_balance')
    def trade_balance():
        fetcher = EconomicDataFetcher()
        try:
            trade_balance_data = fetcher.fetch_trade_balance_data()
            years = [entry['year'] for entry in trade_balance_data]
            trade_balance_values = [entry['trade_balance'] for entry in trade_balance_data]
            return render_template('trade_balance.html', labels=years, data=trade_balance_values)
        except requests.RequestException as e:
            flash(f"Error fetching trade balance data: {e}", 'danger')
            return render_template('trade_balance.html', labels=[], data=[])

    @app.route('/unemployment')
    def unemployment():
        fetcher = EconomicDataFetcher()
        try:
            unemployment_data = fetcher.fetch_unemployment_data()
            years = [entry['year'] for entry in unemployment_data]
            unemployment_values = [entry['unemployment_rate'] for entry in unemployment_data]
            return render_template('unemployment.html', labels=years, data=unemployment_values)
        except requests.RequestException as e:
            flash(f"Error fetching unemployment data: {e}", 'danger')
            return render_template('unemployment.html', labels=[], data=[])

    @app.route('/govt_spending')
    def govt_spending():
        fetcher = EconomicDataFetcher()
        try:
            govt_spending_data = fetcher.fetch_govt_spending_data()
            years = [entry['year'] for entry in govt_spending_data]
            govt_spending_values = [entry['govt_spending'] for entry in govt_spending_data]
            return render_template('govt_spending.html', labels=years, data=govt_spending_values)
        except requests.RequestException as e:
            flash(f"Error fetching government spending data: {e}", 'danger')
            return render_template('govt_spending.html', labels=[], data=[])

    @app.route('/inflation')
    def inflation():
        fetcher = EconomicDataFetcher()
        try:
            inflation_data = fetcher.fetch_inflation_data()
            years = [entry['year'] for entry in inflation_data]
            inflation_values = [entry['inflation_rate'] for entry in inflation_data]
            return render_template('inflation.html', labels=years, data=inflation_values)
        except requests.RequestException as e:
            flash(f"Error fetching inflation data: {e}", 'danger')
            return render_template('inflation.html', labels=[], data=[])

    @app.route('/interest_rates')
    def interest_rates():
        fetcher = EconomicDataFetcher()
        try:
            interest_rates_data = fetcher.fetch_interest_rates_data()
            years = [entry['year'] for entry in interest_rates_data]
            interest_rates_values = [entry['interest_rate'] for entry in interest_rates_data]
            return render_template('int_rates.html', labels=years, data=interest_rates_values)
        except requests.RequestException as e:
            flash(f"Error fetching interest rates data: {e}", 'danger')
            return render_template('int_rates.html', labels=[], data=[])

    @app.route('/exchange_rates')
    def exchange_rates():
        fetcher = EconomicDataFetcher()
        try:
            exchange_rates_data = fetcher.fetch_exchange_rates_data()
            years = [entry['year'] for entry in exchange_rates_data]
            exchange_rates_values = [entry['exchange_rate'] for entry in exchange_rates_data]
            return render_template('exchange_rate.html', labels=years, data=exchange_rates_values)
        except requests.RequestException as e:
            flash(f"Error fetching exchange rates data: {e}", 'danger')
            return render_template('exchange_rate.html', labels=[], data=[])
