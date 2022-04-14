from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, DetailView

from reservation_system.common.forms import MakeOrderForm
from reservation_system.common.models import MakeOrder

from reservation_system.core.views import BootStrapFormViewMixin, PostOnlyView

from reservation_system.inventory.models import Table
from reservation_system.menu.models import Menu


class TablesView(ListView):
    template_name = 'tables/list_tables.html'
    model = Table
    context_object_name = 'tables'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['orders'] = MakeOrder.objects.all()

        return context


class AddTableView(LoginRequiredMixin, BootStrapFormViewMixin, CreateView):
    model = Table
    fields = ('name', 'description', 'type')
    success_url = reverse_lazy('list tables')
    template_name = 'tables/create_table.html'

    def form_valid(self, form):
        table = form.save(commit=False)
        table.user = self.request.user
        table.save()
        return super().form_valid(form)


class DeleteTableView(LoginRequiredMixin, DeleteView):
    template_name = 'tables/delete_table.html'
    model = Table
    success_url = reverse_lazy('list tables')


# class TableDetailsView(DetailView):
#     model = Table
#     template_name = 'tables/table_details.html'
#     context_object_name = 'table'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         table = context['table']
#         is_owner = table.user == self.request.user
#         context['comment_form'] = CommentForm(
#             initial={
#                 'table_pk': self.object.id,
#             }
#         )
#         context['comments'] = table.comment_set.all()
#         context['is_owner'] = is_owner
#
#         name_order = MakeOrder.objects.all()
#         context['name_o'] = name_order
#         context['make_order_form'] = MakeOrderForm(
#             initial={
#                 'table_pk': self.object.id,
#             }
#         )
#
#         return context

def TableDetailsView(request, pk):
    table = Table.objects.get(pk=pk)
    menu = Menu.objects.all()

    profit = 0
    for order in table.makeorder_set.all():
        for product in menu:
            if order.product == product:
                profit += product.price

    context = {
        'table': table,
        'make_order_form': MakeOrderForm(),
        'orders': table.makeorder_set.all(),
        'menu': menu,
        'profit': profit,
    }

    return render(request, 'tables/table_details.html', context)


# class CommentTableView(LoginRequiredMixin, PostOnlyView):
#     form_class = CommentForm
#
#     def form_valid(self, form):
#         comment = Table.objects.get(pk=self.kwargs['pk'])
#
#         commenting = Comment(
#             text=form.cleaned_data['text'],
#             comment=comment,
#             user=self.request.user,
#
#
#         )
#         commenting.save()
#
#         return redirect('table details', comment.id)
#
#     def form_invalid(self, form):
#         pass


def make_order(request, pk):
    order = Table.objects.get(pk=pk)
    form = MakeOrderForm(request.POST)
    #product = Menu.objects.all()

    if form.is_valid():
        ordering = MakeOrder(
            product=form.cleaned_data['product'],
            order=order,
            #product=product
        )
        ordering.save()
    return redirect('table details', order.id)


# class CreateTableOrderView(LoginRequiredMixin, BootStrapFormViewMixin, CreateView):
#     model = CreateTableOrder
#     fields = ('name',)
#     success_url = reverse_lazy('list tables')
#     template_name = 'tables/create_table_order.html'


class DeleteOrderView(LoginRequiredMixin, DeleteView):

    template_name = 'tables/delete_order.html'
    model = MakeOrder
    success_url = reverse_lazy('list tables')
    context_object_name = 'order'


    # def get_success_url(self):
    #     return reverse('table details', kwargs={'pk': self.get_context_data()['order'].pk})

    # def get_success_url(self):
    #     orderid = self.kwargs['pk']
    #     return reverse_lazy('table details', kwargs={'pk': orderid})


def delete_all_orders(request, pk):
    table = Table.objects.get(pk=pk)
    orders = table.makeorder_set.all()
    if request.method == 'POST':
        orders.delete()
        return redirect('list tables')
    else:
        context = {
            'orders': orders,
        }
        return render(request, 'tables/delete_all_orders.html', context)
