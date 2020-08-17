# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, MetaData, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    number = Column(String(45), nullable=False, unique=True)
    note = Column(String(200))
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    number = Column(String(45), nullable=False, unique=True)
    note = Column(String(200))
    fk_company_id = Column(ForeignKey('company.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(String(45))
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_company = relationship(
        'Company', primaryjoin='Department.fk_company_id == Company.id', backref='departments')


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    number = Column(String(45), nullable=False, unique=True)
    note = Column(String(200))
    fk_department_id = Column(ForeignKey('department.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_department = relationship(
        'Department', primaryjoin='Employee.fk_department_id == Department.id', backref='employees')


class MsssFileResource(Base):
    __tablename__ = 'msss_file_resource'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    host = Column(String(64))
    path = Column(String(512), nullable=False)
    disabled = Column(Integer, server_default=FetchedValue())
    operator_id = Column(ForeignKey('user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    note = Column(String(200))

    operator = relationship(
        'User', primaryjoin='MsssFileResource.operator_id == User.id', backref='msss_file_resources')


class MsssSession(Base):
    __tablename__ = 'msss_session'

    id = Column(Integer, primary_key=True)
    instance_id = Column(String(45), nullable=False, unique=True)
    name = Column(String(64))
    init_time = Column(DateTime, nullable=False, server_default=FetchedValue())
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Integer, nullable=False, server_default=FetchedValue(
    ), info='0: Created;\\n1: Started;\\n2: Crashed;\\n3: UserCanceled;\\n4: Finished;')
    note = Column(String(200))


class MsssSessionInput(Base):
    __tablename__ = 'msss_session_input'

    id = Column(Integer, primary_key=True)
    fk_session_id = Column(ForeignKey('msss_session.id'),
                           nullable=False, index=True)
    module_name = Column(String(128))
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    value = Column(String(1024))

    fk_session = relationship(
        'MsssSession', primaryjoin='MsssSessionInput.fk_session_id == MsssSession.id', backref='msss_session_inputs')


class MsssSessionOutput(Base):
    __tablename__ = 'msss_session_output'

    id = Column(Integer, primary_key=True)
    fk_session_id = Column(ForeignKey('msss_session.id'),
                           nullable=False, index=True)
    module_name = Column(String(128))
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    value = Column(String(1024))

    fk_session = relationship(
        'MsssSession', primaryjoin='MsssSessionOutput.fk_session_id == MsssSession.id', backref='msss_session_outputs')


class MsswFileResource(Base):
    __tablename__ = 'mssw_file_resource'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    host = Column(String(64))
    path = Column(String(512), nullable=False)
    disabled = Column(Integer, server_default=FetchedValue())
    operator_id = Column(ForeignKey('user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    note = Column(String(200))

    operator = relationship(
        'User', primaryjoin='MsswFileResource.operator_id == User.id', backref='mssw_file_resources')


class MsswProgram(Base):
    __tablename__ = 'mssw_program'
    __table_args__ = (
        Index('index', 'fk_utility_id', 'version'),
    )

    id = Column(Integer, primary_key=True)
    fk_utility_id = Column(ForeignKey('mssw_utility.id'),
                           nullable=False, index=True)
    version = Column(String(45), nullable=False)
    fk_provider_employee_id = Column(ForeignKey('employee.id'), index=True)
    description = Column(String(200))
    operator_id = Column(ForeignKey('user.id'), index=True, info='User ID.')
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())

    fk_provider_employee = relationship(
        'Employee', primaryjoin='MsswProgram.fk_provider_employee_id == Employee.id', backref='mssw_programs')
    fk_utility = relationship(
        'MsswUtility', primaryjoin='MsswProgram.fk_utility_id == MsswUtility.id', backref='mssw_programs')
    operator = relationship(
        'User', primaryjoin='MsswProgram.operator_id == User.id', backref='mssw_programs')


class MsswProgramActivation(Base):
    __tablename__ = 'mssw_program_activation'

    id = Column(Integer, primary_key=True)
    fk_program_id = Column(ForeignKey('mssw_program.id'),
                           nullable=False, index=True)
    fk_dict_activate_type = Column(ForeignKey(
        'pub_dict.id'), nullable=False, index=True)
    is_active = Column(Integer, nullable=False, server_default=FetchedValue())
    note = Column(String(45))
    operator_id = Column(ForeignKey('user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    pub_dict = relationship(
        'PubDict', primaryjoin='MsswProgramActivation.fk_dict_activate_type == PubDict.id', backref='mssw_program_activations')
    fk_program = relationship(
        'MsswProgram', primaryjoin='MsswProgramActivation.fk_program_id == MsswProgram.id', backref='mssw_program_activations')
    operator = relationship(
        'User', primaryjoin='MsswProgramActivation.operator_id == User.id', backref='mssw_program_activations')


class MsswProgramConfig(Base):
    __tablename__ = 'mssw_program_config'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    fk_program_id = Column(ForeignKey('mssw_program.id'),
                           nullable=False, index=True)
    module_name = Column(String(64))
    key = Column(String(64))
    index = Column(Integer, nullable=False)
    data_type = Column(Integer)
    value = Column(String(
        1024), info='Type 1: json string;\\nType 2: file path with host address;')
    operator_id = Column(ForeignKey('user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    disabled = Column(Integer, server_default=FetchedValue())

    fk_program = relationship(
        'MsswProgram', primaryjoin='MsswProgramConfig.fk_program_id == MsswProgram.id', backref='mssw_program_configs')
    operator = relationship(
        'User', primaryjoin='MsswProgramConfig.operator_id == User.id', backref='mssw_program_configs')


class MsswProgramConfigAcces(Base):
    __tablename__ = 'mssw_program_config_access'

    id = Column(Integer, primary_key=True)
    fk_program_config_id = Column(ForeignKey(
        'mssw_program_config.id'), nullable=False, index=True)
    department_id = Column(ForeignKey('department.id'), nullable=False, index=True,
                           info='1: target_id => User ID\\n2: target_id => Department ID')
    user_id = Column(ForeignKey('user.id'), index=True)
    operator_id = Column(ForeignKey('user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    disabled = Column(Integer, server_default=FetchedValue())

    department = relationship(
        'Department', primaryjoin='MsswProgramConfigAcces.department_id == Department.id', backref='mssw_program_config_access')
    fk_program_config = relationship(
        'MsswProgramConfig', primaryjoin='MsswProgramConfigAcces.fk_program_config_id == MsswProgramConfig.id', backref='mssw_program_config_access')
    operator = relationship('User', primaryjoin='MsswProgramConfigAcces.operator_id == User.id',
                            backref='user_mssw_program_config_access')
    user = relationship('User', primaryjoin='MsswProgramConfigAcces.user_id == User.id',
                        backref='user_mssw_program_config_access_0')


class MsswTask(Base):
    __tablename__ = 'mssw_task'

    id = Column(Integer, primary_key=True)
    fk_program_id = Column(ForeignKey('mssw_program.id'),
                           nullable=False, index=True)
    fk_program_config_id = Column(ForeignKey(
        'mssw_program_config.id'), index=True)
    status = Column(Integer)
    processor_id = Column(ForeignKey('user.id'), index=True)
    start_time = Column(DateTime, nullable=False,
                        server_default=FetchedValue())
    finish_time = Column(DateTime)
    note = Column(String(200))

    fk_program_config = relationship(
        'MsswProgramConfig', primaryjoin='MsswTask.fk_program_config_id == MsswProgramConfig.id', backref='mssw_tasks')
    fk_program = relationship(
        'MsswProgram', primaryjoin='MsswTask.fk_program_id == MsswProgram.id', backref='mssw_tasks')
    processor = relationship(
        'User', primaryjoin='MsswTask.processor_id == User.id', backref='mssw_tasks')


class MsswTaskInput(Base):
    __tablename__ = 'mssw_task_input'
    __table_args__ = (
        Index('index', 'fk_task_id', 'index'),
    )

    id = Column(Integer, primary_key=True)
    fk_task_id = Column(ForeignKey('mssw_task.id'), nullable=False)
    module_name = Column(String(64))
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    value = Column(String(1024), info='Put json config/list here.')

    fk_task = relationship(
        'MsswTask', primaryjoin='MsswTaskInput.fk_task_id == MsswTask.id', backref='mssw_task_inputs')


class MsswTaskOutput(Base):
    __tablename__ = 'mssw_task_output'
    __table_args__ = (
        Index('po_index', 'fk_task_id', 'index'),
    )

    id = Column(Integer, primary_key=True)
    fk_task_id = Column(ForeignKey('mssw_task.id'), nullable=False, index=True)
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    value = Column(String(1024), info='Put json config/list here.')

    fk_task = relationship(
        'MsswTask', primaryjoin='MsswTaskOutput.fk_task_id == MsswTask.id', backref='mssw_task_outputs')


class MsswTaskRecordAcces(Base):
    __tablename__ = 'mssw_task_record_access'

    id = Column(Integer, primary_key=True)
    fk_task_id = Column(ForeignKey('mssw_task.id'), nullable=False, index=True)
    fk_dict_record_type = Column(ForeignKey(
        'pub_dict.id'), nullable=False, index=True)
    user_id = Column(Integer)
    department_id = Column(Integer)
    disabled = Column(Integer, server_default=FetchedValue())
    operator_id = Column(ForeignKey('user.id'), index=True)
    operate_time = Column(DateTime, server_default=FetchedValue())

    pub_dict = relationship(
        'PubDict', primaryjoin='MsswTaskRecordAcces.fk_dict_record_type == PubDict.id', backref='mssw_task_record_access')
    fk_task = relationship(
        'MsswTask', primaryjoin='MsswTaskRecordAcces.fk_task_id == MsswTask.id', backref='mssw_task_record_access')
    operator = relationship(
        'User', primaryjoin='MsswTaskRecordAcces.operator_id == User.id', backref='mssw_task_record_access')


class MsswUtility(Base):
    __tablename__ = 'mssw_utility'
    __table_args__ = (
        Index('utility_fk_dict_sub_group_id_2_pub_dict_idx',
              'fk_dict_utility_main_group_id', 'fk_dict_utility_sub_group_id'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    display_name = Column(String(128), nullable=False)
    fk_dict_utility_main_group_id = Column(
        ForeignKey('pub_dict.id'), nullable=False, index=True)
    fk_dict_utility_sub_group_id = Column(
        ForeignKey('pub_dict.id'), nullable=False, index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(ForeignKey('user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    description = Column(String(200))

    fk_dict_utility_main_group = relationship(
        'PubDict', primaryjoin='MsswUtility.fk_dict_utility_main_group_id == PubDict.id', backref='pubdict_mssw_utilities')
    fk_dict_utility_sub_group = relationship(
        'PubDict', primaryjoin='MsswUtility.fk_dict_utility_sub_group_id == PubDict.id', backref='pubdict_mssw_utilities_0')
    operator = relationship(
        'User', primaryjoin='MsswUtility.operator_id == User.id', backref='mssw_utilities')


class PubDict(Base):
    __tablename__ = 'pub_dict'
    __table_args__ = (
        Index('index', 'name', 'category'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    category = Column(String(45), nullable=False)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    note = Column(String(200))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    email = Column(String(64))
    fk_employee_id = Column(ForeignKey('employee.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_employee = relationship(
        'Employee', primaryjoin='User.fk_employee_id == Employee.id', backref='users')
