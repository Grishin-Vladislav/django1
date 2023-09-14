import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture(scope='module')
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def courses(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return courses


@pytest.mark.django_db
def test_get_certain_course(client, courses_factory):
    course = courses_factory()
    # #
    #     from django import urls
    #
    #     url_resolver = urls.get_resolver(urls.get_urlconf())
    #     print(url_resolver.namespace_dict.items())
    #
    # url = reverse('students:courses-list')
    response = client.get(
        f'/api/v1/courses/{course.id}/'
    )

    assert response.status_code == 200
    assert response.json()['name'] == course.name


@pytest.mark.django_db
def test_get_courses_list(client, courses_factory):
    courses = courses_factory(_quantity=100)

    response = client.get(f'/api/v1/courses/')

    assert response.status_code == 200
    for index, course in enumerate(response.json()):
        assert course['name'] == courses[index].name


@pytest.mark.django_db
def test_filter_by_id(client, courses_factory):
    courses = courses_factory(_quantity=10)

    for course in courses:
        response = client.get(f'/api/v1/courses/?id={course.id}')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_filter_by_name(client, courses_factory):
    courses = courses_factory(_quantity=10)

    for course in courses:
        response = client.get(f'/api/v1/courses/?name={course.name}')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course():
    c_id = 123
    c_name = 'python'

    stud = Student(id=1, name='stud1', birth_date='2010-10-10')
    stud.save()

    course = Course(id=c_id, name=c_name)
    course.save()
    course.students.set([stud])

    query = Course.objects.all()
    course = query[0]

    assert len(query) == 1
    assert course.id == c_id
    assert course.name == c_name
    assert course.students.count() == 1
    assert isinstance(course.students.first(), Student)


@pytest.mark.django_db
def test_update_course(client, courses_factory):
    course = courses_factory()
    data = {'name': 'python'}

    response = client.patch(f'/api/v1/courses/{course.id}/',
                            data=data,
                            format='json')

    assert response.status_code == 200
    assert response.json()['name'] == data['name']


@pytest.mark.django_db
def test_destroy_course(client, courses_factory):
    course = courses_factory()

    response = client.delete(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 204
    assert Course.objects.count() == 0