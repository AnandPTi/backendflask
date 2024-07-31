def test_get_assignments(client, headers, expected_student_id):
    response = client.get(
        '/student/assignments',
        headers=headers
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == expected_student_id


def test_get_assignments_student_1(client, h_student_1):
    test_get_assignments(client, h_student_1, 1)


def test_get_assignments_student_2(client, h_student_2):
    test_get_assignments(client, h_student_2, 2)


def test_post_assignment(client, headers, content, expected_status, expected_state=None, expected_teacher_id=None):
    response = client.post(
        '/student/assignments',
        headers=headers,
        json={
            'content': content
        }
    )

    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.json['data']
        assert data['content'] == content
        assert data['state'] == expected_state
        assert data['teacher_id'] == expected_teacher_id


def test_post_assignment_null_content(client, h_student_1):
    """
    Failure case: content cannot be null
    """
    test_post_assignment(client, h_student_1, None, 400)


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'
    test_post_assignment(client, h_student_1, content, 200, 'DRAFT')


def test_submit_assignment(client, headers, assignment_id, teacher_id, expected_student_id, expected_state):
    response = client.post(
        '/student/assignments/submit',
        headers=headers,
        json={
            'id': assignment_id,
            'teacher_id': teacher_id
        }
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == expected_student_id
    assert data['state'] == expected_state
    assert data['teacher_id'] == teacher_id


def test_submit_assignment_student_1(client, h_student_1):
    test_submit_assignment(client, h_student_1, 2, 2, 1, 'SUBMITTED')


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )

    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'only a draft assignment can be submitted'
