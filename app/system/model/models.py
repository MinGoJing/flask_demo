# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


# db
from app import db


class SysCompany(db.Model):
    __tablename__ = 'sys_company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    note = db.Column(db.String(200))
    disabled = db.Column(db.Integer, nullable=False,
                         server_default=db.FetchedValue())
    operator_id = db.Column(db.Integer)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())


class SysDepartment(db.Model):
    __tablename__ = 'sys_department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    note = db.Column(db.String(200))
    fk_sys_company_id = db.Column(db.ForeignKey('sys_company.id'), index=True)
    disabled = db.Column(db.Integer, nullable=False,
                         server_default=db.FetchedValue())
    operator_id = db.Column(db.String(45))
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())

    fk_sys_company = db.relationship(
        'SysCompany', primaryjoin='SysDepartment.fk_sys_company_id == SysCompany.id', backref='sys_departments')


class SysEmployee(db.Model):
    __tablename__ = 'sys_employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    note = db.Column(db.String(200))
    fk_sys_department_id = db.Column(
        db.ForeignKey('sys_department.id'), index=True)
    disabled = db.Column(db.Integer, nullable=False,
                         server_default=db.FetchedValue())
    operator_id = db.Column(db.Integer)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())

    fk_sys_department = db.relationship(
        'SysDepartment', primaryjoin='SysEmployee.fk_sys_department_id == SysDepartment.id', backref='sys_employees')


class SysUser(db.Model):
    __tablename__ = 'sys_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64))
    fk_sys_employee_id = db.Column(
        db.ForeignKey('sys_employee.id'), index=True)
    disabled = db.Column(db.Integer, nullable=False,
                         server_default=db.FetchedValue())
    operator_id = db.Column(db.Integer)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())

    fk_sys_employee = db.relationship(
        'SysEmployee', primaryjoin='SysUser.fk_sys_employee_id == SysEmployee.id', backref='sys_users')
