# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


#
from app import db


class MsswFileResource(db.Model):
    __tablename__ = 'mssw_file_resource'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    host = db.Column(db.String(64))
    fulll_path = db.Column(db.String(512), nullable=False)
    disabled = db.Column(db.Integer, server_default=db.FetchedValue())
    operator_id = db.Column(db.ForeignKey('sys_user.id'), index=True)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())
    note = db.Column(db.String(200))

    operator = db.relationship(
        'SysUser', primaryjoin='MsswFileResource.operator_id == SysUser.id', backref='mssw_file_resources')


class MsswProces(db.Model):
    __tablename__ = 'mssw_process'

    id = db.Column(db.Integer, primary_key=True)
    fk_program_id = db.Column(db.ForeignKey(
        'mssw_program.id'), nullable=False, index=True)
    fk_program_config_id = db.Column(
        db.ForeignKey('mssw_program_config.id'), index=True)
    status = db.Column(db.Integer)
    processor_id = db.Column(db.Integer)
    start_time = db.Column(db.DateTime, nullable=False,
                           server_default=db.FetchedValue())
    finish_time = db.Column(db.DateTime)
    note = db.Column(db.String(200))

    fk_program_config = db.relationship(
        'MsswProgramConfig', primaryjoin='MsswProces.fk_program_config_id == MsswProgramConfig.id', backref='mssw_process')
    fk_program = db.relationship(
        'MsswProgram', primaryjoin='MsswProces.fk_program_id == MsswProgram.id', backref='mssw_process')


class MsswProcessModelInput(db.Model):
    __tablename__ = 'mssw_process_model_input'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    index = db.Column(db.Integer, nullable=False, unique=True,
                      server_default=db.FetchedValue())
    fk_process_id = db.Column(db.Integer, nullable=False, unique=True)
    note = db.Column(db.String(200))


class MsswProcessModelInputValue(db.Model):
    __tablename__ = 'mssw_process_model_input_value'

    id = db.Column(db.Integer, primary_key=True)
    fk_process_model_input_id = db.Column(db.ForeignKey(
        'mssw_process_model_input.id'), nullable=False, index=True)
    key = db.Column(db.String(64), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    data_type = db.Column(db.Integer, nullable=False)
    v1 = db.Column(db.String(64))
    v2 = db.Column(db.String(64))
    v3 = db.Column(db.String(512), info='Put json config/list here.')

    fk_process_model_input = db.relationship(
        'MsswProcessModelInput', primaryjoin='MsswProcessModelInputValue.fk_process_model_input_id == MsswProcessModelInput.id', backref='mssw_process_model_input_values')


class MsswProcessModelLog(db.Model):
    __tablename__ = 'mssw_process_model_log'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    index = db.Column(db.Integer, nullable=False, unique=True,
                      server_default=db.FetchedValue())
    fk_process_id = db.Column(db.Integer, nullable=False, unique=True)
    note = db.Column(db.String(200))


class MsswProcessModelLogValue(db.Model):
    __tablename__ = 'mssw_process_model_log_value'

    id = db.Column(db.Integer, primary_key=True)
    fk_process_model_log_id = db.Column(db.ForeignKey(
        'mssw_process_model_log.id'), nullable=False, index=True)
    key = db.Column(db.String(64), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    data_type = db.Column(db.Integer, nullable=False)
    v1 = db.Column(db.String(64))
    v2 = db.Column(db.String(64))
    v3 = db.Column(db.String(512), info='Put json config/list here.')

    fk_process_model_log = db.relationship(
        'MsswProcessModelLog', primaryjoin='MsswProcessModelLogValue.fk_process_model_log_id == MsswProcessModelLog.id', backref='mssw_process_model_log_values')


class MsswProcessModelOutput(db.Model):
    __tablename__ = 'mssw_process_model_output'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    index = db.Column(db.Integer, nullable=False, unique=True,
                      server_default=db.FetchedValue())
    fk_process_id = db.Column(db.Integer, nullable=False, unique=True)
    note = db.Column(db.String(200))


class MsswProcessModelOutputValue(db.Model):
    __tablename__ = 'mssw_process_model_output_value'

    id = db.Column(db.Integer, primary_key=True)
    fk_process_model_output_id = db.Column(db.ForeignKey(
        'mssw_process_model_output.id'), nullable=False, index=True)
    key = db.Column(db.String(64), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    data_type = db.Column(db.Integer, nullable=False)
    v1 = db.Column(db.String(64))
    v2 = db.Column(db.String(64))
    v3 = db.Column(db.String(512), info='Put json config/list here.')

    fk_process_model_output = db.relationship(
        'MsswProcessModelOutput', primaryjoin='MsswProcessModelOutputValue.fk_process_model_output_id == MsswProcessModelOutput.id', backref='mssw_process_model_output_values')


class MsswProcessModelParameter(db.Model):
    __tablename__ = 'mssw_process_model_parameter'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    index = db.Column(db.Integer, nullable=False, unique=True,
                      server_default=db.FetchedValue())
    fk_process_id = db.Column(db.Integer, nullable=False, unique=True)
    note = db.Column(db.String(200))


class MsswProcessModelParameterValue(db.Model):
    __tablename__ = 'mssw_process_model_parameter_value'

    id = db.Column(db.Integer, primary_key=True)
    fk_process_model_parameter_id = db.Column(db.ForeignKey(
        'mssw_process_model_parameter.id'), nullable=False, index=True)
    key = db.Column(db.String(64), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    data_type = db.Column(db.Integer, nullable=False)
    v1 = db.Column(db.String(64))
    v2 = db.Column(db.String(64))
    v3 = db.Column(db.String(512), info='Put json config/list here.')

    fk_process_model_parameter = db.relationship(
        'MsswProcessModelParameter', primaryjoin='MsswProcessModelParameterValue.fk_process_model_parameter_id == MsswProcessModelParameter.id', backref='mssw_process_model_parameter_values')


class MsswProcessRecordAcces(db.Model):
    __tablename__ = 'mssw_process_record_access'

    id = db.Column(db.Integer, primary_key=True)
    fk_process_id = db.Column(db.ForeignKey(
        'mssw_process.id'), nullable=False, index=True)
    fk_dict_record_type = db.Column(db.ForeignKey(
        'pub_dict.id'), nullable=False, index=True)
    target_type = db.Column(db.Integer, nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    disabled = db.Column(db.Integer, server_default=db.FetchedValue())
    operator_id = db.Column(db.ForeignKey('sys_user.id'), index=True)
    operate_time = db.Column(db.DateTime, server_default=db.FetchedValue())

    pub_dict = db.relationship(
        'PubDict', primaryjoin='MsswProcessRecordAcces.fk_dict_record_type == PubDict.id', backref='mssw_process_record_access')
    fk_process = db.relationship(
        'MsswProces', primaryjoin='MsswProcessRecordAcces.fk_process_id == MsswProces.id', backref='mssw_process_record_access')
    operator = db.relationship(
        'SysUser', primaryjoin='MsswProcessRecordAcces.operator_id == SysUser.id', backref='mssw_process_record_access')


class MsswProgram(db.Model):
    __tablename__ = 'mssw_program'

    id = db.Column(db.Integer, primary_key=True)
    fk_utility_id = db.Column(db.ForeignKey(
        'mssw_ultility.id'), nullable=False, index=True)
    version = db.Column(db.String(45), nullable=False)
    fk_provider_employee_id = db.Column(
        db.ForeignKey('sys_employee.id'), index=True)
    fk_parent_program_id = db.Column(
        db.ForeignKey('mssw_program.id'), index=True)
    description = db.Column(db.String(200))
    operator_id = db.Column(db.ForeignKey('sys_user.id'),
                            index=True, info='User ID.')
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())
    disabled = db.Column(db.Integer, nullable=False,
                         server_default=db.FetchedValue())

    fk_parent_program = db.relationship('MsswProgram', remote_side=[
                                        id], primaryjoin='MsswProgram.fk_parent_program_id == MsswProgram.id', backref='mssw_programs')
    fk_provider_employee = db.relationship(
        'SysEmployee', primaryjoin='MsswProgram.fk_provider_employee_id == SysEmployee.id', backref='mssw_programs')
    fk_utility = db.relationship(
        'MsswUltility', primaryjoin='MsswProgram.fk_utility_id == MsswUltility.id', backref='mssw_programs')
    operator = db.relationship(
        'SysUser', primaryjoin='MsswProgram.operator_id == SysUser.id', backref='mssw_programs')


class MsswProgramActivation(db.Model):
    __tablename__ = 'mssw_program_activation'

    id = db.Column(db.Integer, primary_key=True)
    fk_program_id = db.Column(db.ForeignKey(
        'mssw_program.id'), nullable=False, index=True)
    fk_dict_activate_type = db.Column(db.ForeignKey(
        'pub_dict.id'), nullable=False, index=True)
    is_active = db.Column(db.Integer, nullable=False,
                          server_default=db.FetchedValue())
    note = db.Column(db.String(45))
    operator_id = db.Column(db.ForeignKey('sys_user.id'), index=True)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())

    pub_dict = db.relationship(
        'PubDict', primaryjoin='MsswProgramActivation.fk_dict_activate_type == PubDict.id', backref='mssw_program_activations')
    fk_program = db.relationship(
        'MsswProgram', primaryjoin='MsswProgramActivation.fk_program_id == MsswProgram.id', backref='mssw_program_activations')
    operator = db.relationship(
        'SysUser', primaryjoin='MsswProgramActivation.operator_id == SysUser.id', backref='mssw_program_activations')


class MsswProgramConfig(db.Model):
    __tablename__ = 'mssw_program_config'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    fk_program_id = db.Column(db.ForeignKey('mssw_program.id'), db.ForeignKey(
        'mssw_program.id'), nullable=False, index=True)
    fk_dict_program_cfg_type = db.Column(db.ForeignKey(
        'pub_dict.id'), nullable=False, index=True, info='1: json string\\n2: config file')
    config_value = db.Column(db.String(
        2048), info='Type 1: json string;\\nType 2: file path with host address;')
    operator_id = db.Column(db.ForeignKey('sys_user.id'),
                            db.ForeignKey('sys_user.id'), index=True)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())
    disabled = db.Column(db.Integer, server_default=db.FetchedValue())

    pub_dict = db.relationship(
        'PubDict', primaryjoin='MsswProgramConfig.fk_dict_program_cfg_type == PubDict.id', backref='mssw_program_configs')
    fk_program = db.relationship(
        'MsswProgram', primaryjoin='MsswProgramConfig.fk_program_id == MsswProgram.id', backref='msswprogram_mssw_program_configs')
    fk_program1 = db.relationship(
        'MsswProgram', primaryjoin='MsswProgramConfig.fk_program_id == MsswProgram.id', backref='msswprogram_mssw_program_configs_0')
    operator = db.relationship(
        'SysUser', primaryjoin='MsswProgramConfig.operator_id == SysUser.id', backref='sysuser_mssw_program_configs')
    operator1 = db.relationship(
        'SysUser', primaryjoin='MsswProgramConfig.operator_id == SysUser.id', backref='sysuser_mssw_program_configs_0')


class MsswProgramConfigAcces(db.Model):
    __tablename__ = 'mssw_program_config_access'

    id = db.Column(db.Integer, primary_key=True)
    fk_program_config_id = db.Column(db.ForeignKey('mssw_program_config.id'), db.ForeignKey(
        'mssw_program_config.id'), nullable=False, index=True)
    target_type = db.Column(db.Integer, nullable=False,
                            info='1: target_id => User ID\\n2: target_id => Department ID')
    target_id = db.Column(db.Integer)
    operator_id = db.Column(db.ForeignKey('sys_user.id'), index=True)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())
    disabled = db.Column(db.Integer, server_default=db.FetchedValue())

    fk_program_config = db.relationship(
        'MsswProgramConfig', primaryjoin='MsswProgramConfigAcces.fk_program_config_id == MsswProgramConfig.id', backref='msswprogramconfig_mssw_program_config_access')
    fk_program_config1 = db.relationship(
        'MsswProgramConfig', primaryjoin='MsswProgramConfigAcces.fk_program_config_id == MsswProgramConfig.id', backref='msswprogramconfig_mssw_program_config_access_0')
    operator = db.relationship(
        'SysUser', primaryjoin='MsswProgramConfigAcces.operator_id == SysUser.id', backref='mssw_program_config_access')


class MsswUltility(db.Model):
    __tablename__ = 'mssw_ultility'
    __table_args__ = (
        db.Index('utility_fk_dict_sub_group_id_2_pub_dict_idx',
                 'fk_dict_utility_main_group_id', 'fk_dict_utility_sub_group_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    fk_dict_utility_main_group_id = db.Column(
        db.ForeignKey('pub_dict.id'), nullable=False, index=True)
    fk_dict_utility_sub_group_id = db.Column(
        db.ForeignKey('pub_dict.id'), nullable=False, index=True)
    disabled = db.Column(db.Integer, nullable=False,
                         server_default=db.FetchedValue())
    operator_id = db.Column(db.ForeignKey('sys_user.id'), index=True)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())
    description = db.Column(db.String(200))

    fk_dict_utility_main_group = db.relationship(
        'PubDict', primaryjoin='MsswUltility.fk_dict_utility_main_group_id == PubDict.id', backref='pubdict_mssw_ultilities')
    fk_dict_utility_sub_group = db.relationship(
        'PubDict', primaryjoin='MsswUltility.fk_dict_utility_sub_group_id == PubDict.id', backref='pubdict_mssw_ultilities_0')
    operator = db.relationship(
        'SysUser', primaryjoin='MsswUltility.operator_id == SysUser.id', backref='mssw_ultilities')


class PubDict(db.Model):
    __tablename__ = 'pub_dict'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    category = db.Column(db.String(45), nullable=False)
    disabled = db.Column(db.Integer, nullable=False,
                         server_default=db.FetchedValue())
    operator_id = db.Column(db.Integer)
    operate_time = db.Column(db.DateTime, nullable=False,
                             server_default=db.FetchedValue())
    note = db.Column(db.String(200))


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
