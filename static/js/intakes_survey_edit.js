$(document).ready(function() {

    if($("#id_tp2_ls4_reports_status").is(":checked"))
    {
         $('#id_reports_comments').removeAttr('disabled');
    }
    else
    {
       $('#id_reports_comments').val('');
       $('#id_reports_comments'). attr('disabled','disabled');
    }

    if($("#id_wells_documentation_status").is(":checked"))
    {
         $('#id_wells_documentation_comments').removeAttr('disabled');
    }
    else
    {
       $('#id_wells_documentation_comments').val('');
       $('#id_wells_documentation_comments'). attr('disabled','disabled');
    }

    if($("#id_project_documentation_status").is(":checked"))
    {
         $('#id_project_documentation_comments').removeAttr('disabled');
    }
    else
    {
       $('#id_project_documentation_comments').val('');
       $('#id_project_documentation_comments'). attr('disabled','disabled');
    }

    if($("#id_geophysics_logs_status").is(":checked"))
    {
         $('#id_geophysics_logs_comments').removeAttr('disabled');
    }
    else
    {
       $('#id_geophysics_logs_comments').val('');
       $('#id_geophysics_logs_comments'). attr('disabled','disabled');
    }

    if($("#id_wells_protect_status").is(":checked"))
    {
         $('#id_wells_protect_description').removeAttr('disabled');
    }
    else
    {
       $('#id_wells_protect_description').val('');
       $('#id_wells_protect_description'). attr('disabled','disabled');
    }

    if($("#id_water_treatment_status").is(":checked"))
    {
         $('#id_water_treatment_description').removeAttr('disabled');
    }
    else
    {
       $('#id_water_treatment_description').val('');
       $('#id_water_treatment_description'). attr('disabled','disabled');
    }

    if($("#id_sanitation_zone_status").is(":checked"))
    {
         $('#id_sanitation_zone_description').removeAttr('disabled');
    }
    else
    {
       $('#id_sanitation_zone_description').val('');
       $('#id_sanitation_zone_description'). attr('disabled','disabled');
    }

    if($("#id_contamination_status").is(":checked"))
    {
         $('#id_contamination_description').removeAttr('disabled');
    }
    else
    {
       $('#id_contamination_description').val('');
       $('#id_contamination_description'). attr('disabled','disabled');
    }
});

$('#id_tp2_ls4_reports_status').change(function(){
    if($("#id_tp2_ls4_reports_status").is(":checked"))
    {
         $('#id_reports_comments').removeAttr('disabled');
    }
    else
    {
       $('#id_reports_comments').val('');
       $('#id_reports_comments'). attr('disabled','disabled');
    }
});

$('#id_wells_documentation_status').change(function(){
    if($("#id_wells_documentation_status").is(":checked"))
    {
         $('#id_wells_documentation_comments').removeAttr('disabled');
    }
    else
    {
       $('#id_wells_documentation_comments').val('');
       $('#id_wells_documentation_comments'). attr('disabled','disabled');
    }
});
$('#id_project_documentation_status').change(function(){
    if($("#id_project_documentation_status").is(":checked"))
    {
         $('#id_project_documentation_comments').removeAttr('disabled');
    }
    else
    {
       $('#id_project_documentation_comments').val('');
       $('#id_project_documentation_comments'). attr('disabled','disabled');
    }
});
$('#id_geophysics_logs_status').change(function(){
    if($("#id_geophysics_logs_status").is(":checked"))
    {
         $('#id_geophysics_logs_comments').removeAttr('disabled');
    }
    else
    {
       $('#id_geophysics_logs_comments').val('');
       $('#id_geophysics_logs_comments'). attr('disabled','disabled');
    }
});
$('#id_wells_protect_status').change(function(){
    if($("#id_wells_protect_status").is(":checked"))
    {
         $('#id_wells_protect_description').removeAttr('disabled');
    }
    else
    {
       $('#id_wells_protect_description').val('');
       $('#id_wells_protect_description'). attr('disabled','disabled');
    }
});
$('#id_water_treatment_status').change(function(){
    if($("#id_water_treatment_status").is(":checked"))
    {
         $('#id_water_treatment_description').removeAttr('disabled');
    }
    else
    {
       $('#id_water_treatment_description').val('');
       $('#id_water_treatment_description'). attr('disabled','disabled');
    }
});
$('#id_sanitation_zone_status').change(function(){
    if($("#id_sanitation_zone_status").is(":checked"))
    {
         $('#id_sanitation_zone_description').removeAttr('disabled');
    }
    else
    {
       $('#id_sanitation_zone_description').val('');
       $('#id_sanitation_zone_description'). attr('disabled','disabled');
    }
});
$('#id_contamination_status').change(function(){
    if($("#id_contamination_status").is(":checked"))
    {
         $('#id_contamination_description').removeAttr('disabled');
    }
    else
    {
       $('#id_contamination_description').val('');
       $('#id_contamination_description'). attr('disabled','disabled');
    }
});