# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, MetaData, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class SysCompany(Base):
    __tablename__ = 'sys_company'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    note = Column(String(200))
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())


class SysDepartment(Base):
    __tablename__ = 'sys_department'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    note = Column(String(200))
    fk_sys_company_id = Column(ForeignKey('sys_company.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(String(45))
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_sys_company = relationship(
        'SysCompany', primaryjoin='SysDepartment.fk_sys_company_id == SysCompany.id', backref='sys_departments')


class SysEmployee(Base):
    __tablename__ = 'sys_employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    note = Column(String(200))
    fk_sys_department_id = Column(ForeignKey('sys_department.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_sys_department = relationship(
        'SysDepartment', primaryjoin='SysEmployee.fk_sys_department_id == SysDepartment.id', backref='sys_employees')


class SysUser(Base):
    __tablename__ = 'sys_user'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    email = Column(String(64))
    fk_sys_employee_id = Column(ForeignKey('sys_employee.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_sys_employee = relationship(
        'SysEmployee', primaryjoin='SysUser.fk_sys_employee_id == SysEmployee.id', backref='sys_users')
