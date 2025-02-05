const data = {
  address: address,
  floor: floor,
  full_name: full_name,
  position_at_work: position_at_work,
  computer_name: computer_name,
  work_group: work_group,
  comment: comment
};

const data_edit = {
  address: address,
  floor: floor,
  position_at_work: position_at_work,
  computer_name: computer_name,
  work_group: work_group,
  comment: comment
};

const response = await fetch('http://127.0.0.1:8000/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  },
  body: JSON.stringify(data)
});
return response.json();

const edit = await fetch('http://127.0.0.1:8000/update user', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  },
  body: JSON.stringify(data_edit)
});
return edit.json();