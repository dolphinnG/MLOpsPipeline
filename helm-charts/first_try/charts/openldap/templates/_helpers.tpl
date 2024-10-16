{{- define "openldap.labels" -}}
app: {{ .Release.Name }}-{{ .Chart.Name }} 
{{- end }}

{{- define "openldap.secrets" -}}
{{ .Release.Name }}-ldap-secret
{{- end }}

{{- define "openldap.configmap-init-files" -}}
{{ .Release.Name }}-ldap-config-init-files
{{- end }}

{{- define "openldap.configmap-env" -}}
{{ .Release.Name }}-ldap-config-env
{{- end }}