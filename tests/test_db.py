from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='Felipe',
        password=123,
        email='felipe@test.com'
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'felipe@test.com')
    )

    assert result.username == "Felipe"
