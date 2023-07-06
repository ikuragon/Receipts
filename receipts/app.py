from auth import *
from models import *
from main import *


@app.route('/')
def index():
    receipts = Receipt.query.all()
    return render_template('index.html', receipts=receipts)


@app.route('/add_receipt', methods=['GET', 'POST'])
def add_receipt():
    form = AddReceiptForm()
    if form.validate_on_submit():
        receipt = Receipt(
            name_of_receipt=form.name_of_receipt.data,
            about_of_receipt=form.about_of_receipt.data,
            ingredients=form.ingredients.data,
            kilocalories=form.kilocalories.data,
            author_of_receipt=session['username']
        )
        db.session.add(receipt)
        db.session.commit()
        flash('Рецепт добавлен!', 'success')
        return redirect(url_for('index', receipt_id=receipt.id))
    return render_template('add_receipt.html', form=form)


@app.route('/delete_receipt/<int:receipt_id>', methods=['POST'])
def delete_receipt(receipt_id):
    receipt_to_delete = Receipt.query.get_or_404(receipt_id)
    if receipt_to_delete.author_of_receipt != session.get('username'):
        flash('Вы не автор рецепта', 'danger')
        return redirect(url_for('index'))
    db.session.delete(receipt_to_delete)
    db.session.commit()
    flash('Рецепт успешно удален', 'success')
    return redirect(url_for('index'))


@app.route('/edit_receipt/<int:receipt_id>', methods=['GET', 'POST'])
def edit_receipt(receipt_id):
    receipt = Receipt.query.get_or_404(receipt_id)
    if receipt.author_of_receipt != session.get('username'):
        flash('Вы не автор рецепта', 'danger')
        return redirect(url_for('index'))
    form = AddReceiptForm(obj=receipt)
    if form.validate_on_submit():
        form.populate_obj(receipt)
        db.session.commit()
        flash('Рецепт успешно отредактирован!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_receipt.html', form=form)


@app.route('/view_receipt/<int:receipt_id>', methods=['GET', 'POST'])
def view_receipt(receipt_id):
    receipt = Receipt.query.get_or_404(receipt_id)
    form = RatingForm()
    ratings = Rating.query.filter_by(receipt_id=receipt_id).all()
    if form.validate_on_submit():
        rate = form.rate.data
        comment = form.comment.data
        new_rating = Rating(rate=rate, comment=comment, receipt_id=receipt_id)
        db.session.add(new_rating)
        db.session.commit()
        return redirect(url_for('view_receipt', receipt_id=receipt_id))
    return render_template('view_receipt.html', receipt=receipt, form=form, ratings=ratings)


@app.route('/add_rate/<int:receipt_id>', methods=['POST'])
def add_rate(receipt_id):
    rate = int(request.form.get('rate'))
    if rate > 10:
        return "<script>alert('Ошибка! Цифра выше 10'); window.history.back();</script>"
    comment = request.form['comment']
    new_rating = Rating(rate=rate, comment=comment, receipt_id=receipt_id, rating_user_id=session['username'])
    db.session.add(new_rating)
    db.session.commit()
    return redirect(url_for('view_receipt', receipt_id=receipt_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
